#!/usr/bin/env python3

import argparse
import ipaddress
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile

BACKUP_SUFFIX = '.parkit.bak'
DIRECTORY_URL_RE = re.compile(r'<directoryURL>.*?</directoryURL>')
DIRECTORY_URL_TEMPLATE = '<directoryURL>http://{0}:5001/services</directoryURL>'
LOCATE_PATTERNS = ['/var/*/tftp', '/var/*/tftpboot']


def get_current_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.settimeout(1.0)
        sock.connect(('8.8.8.8', 80))
        return sock.getsockname()[0]
    except OSError as exc:
        print('Error detecting IP address: {}'.format(exc), file=sys.stderr)
        return None
    finally:
        sock.close()


def resolve_ip(explicit_ip):
    candidate = explicit_ip or os.environ.get('PARKIT_HOST', '')
    candidate = candidate.strip()
    if candidate:
        try:
            ipaddress.IPv4Address(candidate)
        except ipaddress.AddressValueError:
            raise ValueError('invalid IPv4 address: {}'.format(candidate))
        return candidate

    detected = get_current_ip()
    if detected:
        print(
            'Warning: auto-detected {}. Use --ip on a multi-homed PBX.'.format(detected),
            file=sys.stderr,
        )
    return detected


def refresh_locate_database():
    try:
        result = subprocess.run(
            ['sudo', 'updatedb'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except OSError as exc:
        print('Warning: could not run updatedb: {}'.format(exc), file=sys.stderr)
        return

    if result.returncode != 0:
        print(
            'Warning: updatedb failed: {}'.format(result.stderr.strip()),
            file=sys.stderr,
        )


def find_tftp_directories():
    try:
        result = subprocess.run(
            ['sudo', 'locate'] + LOCATE_PATTERNS,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except OSError as exc:
        print("Error running 'sudo locate': {}".format(exc), file=sys.stderr)
        return []

    if result.returncode != 0:
        print(
            "Error executing 'sudo locate': {}".format(result.stderr.strip()),
            file=sys.stderr,
        )
        return []

    directories = []
    seen = set()
    for line in result.stdout.splitlines():
        path = line.strip()
        if path and path not in seen and os.path.isdir(path):
            directories.append(path)
            seen.add(path)
    return directories


def iter_config_files(directories):
    seen = set()
    for directory in directories:
        for root, _dirs, files in os.walk(directory):
            for file_name in files:
                if not (file_name.startswith('SEP') and file_name.endswith('.cnf.xml')):
                    continue
                path = os.path.join(root, file_name)
                if path not in seen:
                    seen.add(path)
                    yield path


def iter_backup_files(directories):
    seen = set()
    suffix = '.cnf.xml' + BACKUP_SUFFIX
    for directory in directories:
        for root, _dirs, files in os.walk(directory):
            for file_name in files:
                if not file_name.endswith(suffix):
                    continue
                path = os.path.join(root, file_name)
                if path not in seen:
                    seen.add(path)
                    yield path


def atomic_write(path, content, reference_path=None):
    directory = os.path.dirname(path) or '.'
    metadata_path = path if os.path.exists(path) else reference_path
    source_stat = (
        os.stat(metadata_path)
        if metadata_path and os.path.exists(metadata_path)
        else None
    )

    fd, temp_path = tempfile.mkstemp(
        prefix='.parkit-',
        suffix='.tmp',
        dir=directory,
    )
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as temp_file:
            temp_file.write(content)
        if source_stat is not None:
            os.chmod(temp_path, source_stat.st_mode)
            try:
                os.chown(temp_path, source_stat.st_uid, source_stat.st_gid)
            except PermissionError:
                pass
        os.replace(temp_path, path)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def backup_path(path):
    return path + BACKUP_SUFFIX


def ensure_backup(path):
    backup = backup_path(path)
    if not os.path.exists(backup):
        shutil.copy2(path, backup)
    return backup


def update_file(path, ip, dry_run=False):
    with open(path, 'r', encoding='utf-8', newline='') as config_file:
        content = config_file.read()

    if not DIRECTORY_URL_RE.search(content):
        return 'skipped'

    updated = DIRECTORY_URL_RE.sub(DIRECTORY_URL_TEMPLATE.format(ip), content)
    if updated == content:
        return 'unchanged'

    if dry_run:
        print('Would update {}'.format(path))
        return 'would update'

    backup = ensure_backup(path)
    atomic_write(path, updated)
    print('Updated {} (backup: {})'.format(path, backup))
    return 'updated'


def restore_file(backup, dry_run=False):
    original = backup[:-len(BACKUP_SUFFIX)]
    with open(backup, 'r', encoding='utf-8', newline='') as backup_file:
        content = backup_file.read()

    if dry_run:
        print('Would restore {} from {}'.format(original, backup))
        return 'would restore'

    atomic_write(original, content, reference_path=backup)
    print('Restored {} from {}'.format(original, backup))
    return 'restored'


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description='Safely update Cisco SEP*.cnf.xml directory URLs for Parkit.'
    )
    parser.add_argument(
        '--ip',
        metavar='ADDRESS',
        help='IPv4 address phones should use to reach Parkit (overrides auto-detection)',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='show changes without writing files',
    )
    parser.add_argument(
        '--restore',
        action='store_true',
        help='restore the .parkit.bak backups',
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    refresh_locate_database()
    directories = find_tftp_directories()
    if not directories:
        print('No TFTP directories found.', file=sys.stderr)
        return 1

    if args.restore:
        backups = list(iter_backup_files(directories))
        if not backups:
            print('No {} backups found.'.format(BACKUP_SUFFIX))
            return 0

        failures = 0
        for backup in backups:
            try:
                restore_file(backup, args.dry_run)
            except (OSError, UnicodeError) as exc:
                print(
                    'Error restoring {}: {}'.format(backup, exc),
                    file=sys.stderr,
                )
                failures += 1
        return 1 if failures else 0

    try:
        ip = resolve_ip(args.ip)
    except ValueError as exc:
        print('Error: {}'.format(exc), file=sys.stderr)
        return 2

    if not ip:
        print('Unable to determine the Parkit IP address. Use --ip.', file=sys.stderr)
        return 1

    print('Using Parkit IP: {}'.format(ip))
    configs = list(iter_config_files(directories))
    if not configs:
        print('No SEP*.cnf.xml files found.')
        return 0

    counts = {}
    failures = 0
    for path in configs:
        try:
            status = update_file(path, ip, args.dry_run)
        except (OSError, UnicodeError) as exc:
            print('Error processing {}: {}'.format(path, exc), file=sys.stderr)
            failures += 1
            continue

        counts[status] = counts.get(status, 0) + 1
        if status in ('skipped', 'unchanged'):
            print('{}: {}'.format(status.capitalize(), path))

    print(
        'Summary: {} updated, {} would update, {} unchanged, {} skipped, {} errors'.format(
            counts.get('updated', 0),
            counts.get('would update', 0),
            counts.get('unchanged', 0),
            counts.get('skipped', 0),
            failures,
        )
    )
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
