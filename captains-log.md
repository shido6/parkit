# Captain's Log — Parkit Audit & Fixes

**Date:** 2026-06-29

## Summary

Audited the Parkit project (FreePBX parked-calls display for Cisco CP-8851 phones) and fixed all identified issues across 8 categories.

## Files Changed

| File | Action | What |
|------|--------|------|
| `parkit11.py` | Rewritten | Env vars for AMI creds/IP, removed global state race condition, fixed `ParkingSpace`/`ParkingLot` fields, better error handling |
| `dirfix.py` | Edited | Removed duplicated dead code (first 31 lines were a broken copy-paste) |
| `runmefirst.sh` | Rewritten | Removed `/bin/bash` from NOPASSWD sudoers (privilege escalation), uses `/etc/sudoers.d/parkit` drop-in |
| `parkitinstaller.sh` | Edited | Removed dead `get_current_ip()`, removed non-existent `asterisk` pip dep, replaced heredoc shell injection vector with direct commands |
| `parkitinstall.py` | **Deleted** | Dead file, carried `# Dont Use Me` comment |
| `.gitignore` | **Created** | Python project ignores |
| `requirements.txt` | **Created** | `flask`, `pyst2` |
| `boom` | Rewritten | Broken one-liner with literal `{current_ip}` → proper script taking MAC argument |
| `README.md` | Edited | `rm parkit` → `rm -rf parkit` |

## Key Fixes

1. **Hardcoded credentials gone** — `AMI_HOST`, `AMI_PORT`, `AMI_USER`, `AMI_PASS` read from environment with fallback defaults
2. **Race condition eliminated** — `parked_calls` is per-request local, not global
3. **Privilege escalation closed** — No more `NOPASSWD: /bin/bash` in sudoers
4. **Correct AMI fields** — Both `ParkingLot` and `ParkingSpace` captured, template shows both
5. **Dead code removed** — ~150 lines of unreachable/broken code cleaned out
