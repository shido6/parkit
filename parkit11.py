import time
import asterisk.manager
from flask import Flask, render_template_string, Response, request

app = Flask(__name__)

parked_calls = []

def event_listener(event, manager):
    if event.name.lower() == 'parkedcall':
        try:
            global parked_calls
            parked_calls.append({
                'Lot': event['ParkingSpace'],  # Use 'ParkingSpace' instead of 'ParkingLot'
                'CallerID': event['ParkeeCallerIDNum']
            })
        except KeyError as e:
            print("KeyError:", e)
            print("Event data:", event.headers)

def get_parked_calls():
    global parked_calls
    parked_calls.clear()

    manager = asterisk.manager.Manager()

    try:
        # Connect and log in to AMI
        manager.connect('192.168.10.49', 5038)
        manager.login('admin', 'ogZlSNOxemZ5')

        # Register an event listener
        manager.register_event('*', event_listener)

        # Send 'ParkedCalls' action and wait for events
        manager.send_action({'Action': 'ParkedCalls'})

        # Wait for a short period to collect events (adjust as necessary)
        time.sleep(2)  # Example delay

        manager.logoff()

    except asterisk.manager.ManagerException as e:
        print('AMI Error:', e)

    return parked_calls

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
    xml = render_template_string(xml_template, parked_calls=calls)
    return Response(xml, mimetype='text/xml'), 200

xml_template = '''<?xml version="1.0" encoding="UTF-8"?>
<CiscoIPPhoneDirectory>
    <Title>Parked Calls</Title>
    <Prompt>Select to see details</Prompt>
    {% for call in parked_calls %}
        <DirectoryEntry>
        <Name>{{ call.CallerID }} (Line {% if call.Lot == '71' %}1{% elif call.Lot == '72' %}2{% elif call.Lot == '73' %}3{% else %}Unknown{% endif %})</Name>  <!-- Display Caller ID and Line number -->
            <Telephone>{{ call.Lot }}</Telephone>
        </DirectoryEntry>
    {% endfor %}
</CiscoIPPhoneDirectory>
'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

