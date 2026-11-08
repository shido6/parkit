#!/usr/bin/env python3
import os
import time
import asterisk.manager
from flask import Flask, render_template_string, Response, request

app = Flask(__name__)

def required_env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f'{name} environment variable is required')
    return value


AMI_HOST = required_env('AMI_HOST')
AMI_USER = required_env('AMI_USER')
AMI_PASS = required_env('AMI_PASS')

try:
    AMI_PORT = int(os.environ.get('AMI_PORT', '5038'))
except ValueError as exc:
    raise RuntimeError('AMI_PORT must be an integer') from exc


def parked_call_from_event(event):
    return {
        'CallerID': event.get('ParkeeCallerIDNum', ''),
        'Space': event.get('ParkingSpace', ''),
        # Asterisk's ParkedCall event uses "Parkinglot", not "ParkingLot".
        'Lot': event.get('Parkinglot', ''),
    }


def get_parked_calls():
    calls = []
    manager = asterisk.manager.Manager()

    try:
        manager.connect(AMI_HOST, AMI_PORT)
        manager.login(AMI_USER, AMI_PASS)

        def event_listener(event, _manager):
            if event.name.lower() == 'parkedcall':
                calls.append(parked_call_from_event(event))

        manager.register_event('ParkedCall', event_listener)
        manager.send_action({'Action': 'ParkedCalls'})
        time.sleep(2)
        manager.logoff()
    except asterisk.manager.ManagerException as e:
        print('AMI Error:', e)
    except Exception as e:
        print('Unexpected error:', e)

    return calls


@app.route('/services')
def services_menu():
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
    <CiscoIPPhoneMenu>
        <Title>Services</Title>
        <MenuItem>
            <Name>Parked Calls</Name>
            <URL>{url_root}parkedcalls</URL>
        </MenuItem>
    </CiscoIPPhoneMenu>'''.format(url_root=request.url_root)
    return Response(xml, mimetype='text/xml'), 200


@app.route('/parkedcalls')
def parked_calls_service():
    calls = get_parked_calls()
    xml = render_template_string(XML_TEMPLATE, parked_calls=calls)
    return Response(xml, mimetype='text/xml'), 200


XML_TEMPLATE = '''<?xml version="1.0" encoding="UTF-8"?>
<CiscoIPPhoneDirectory>
    <Title>Parked Calls</Title>
    <Prompt>Select to see details</Prompt>
    {% for call in parked_calls %}
        <DirectoryEntry>
            <Name>{{ call.CallerID }} (Lot {{ call.Lot }} / Space {{ call.Space }})</Name>
            <Telephone>{{ call.Space }}</Telephone>
        </DirectoryEntry>
    {% endfor %}
</CiscoIPPhoneDirectory>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
