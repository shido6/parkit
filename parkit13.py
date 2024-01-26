import time
import asterisk.manager
from flask import Flask, render_template_string, Response

app = Flask(__name__)

def event_listener(event, manager):
    if event.name.lower() == 'parkedcall':
        try:
            global parked_calls
            parked_calls.append({
                'Lot': event['ParkingSpace'],
                'CallerID': event['ParkeeCallerIDNum']
            })
        except KeyError as e:
            print("KeyError:", e)
            print("Event data:", event.headers)

def get_parked_calls():
    global parked_calls
    parked_calls = []

    manager = asterisk.manager.Manager()

    try:
        # Connect and log in to AMI
        manager.connect('localhost', 5038)
        manager.login('admin', 'password')

        # Register an event listener
        manager.register_event('*', event_listener)

        # Send 'ParkedCalls' action and wait for events
        manager.send_action({'Action': 'ParkedCalls'})

        # Wait for a short period to collect events (adjust as necessary)
        time.sleep(2)  # Example delay

        manager.logoff()
        return parked_calls

    except asterisk.manager.ManagerException as e:
        print('AMI Error:', e)
        return []

# XML Template and Flask route as before

xml_template = '''<?xml version="1.0" encoding="UTF-8"?>
<CiscoIPPhoneDirectory>
    <Title>Parked Calls</Title>
    <Prompt>Select to see details</Prompt>
    {% for call in parked_calls %}
        <DirectoryEntry>
        <Name>{{ call.CallerID }}</Name>
        <Telephone>{{ get_line(call.Lot) }}</Telephone>
        </DirectoryEntry>
    {% endfor %}
</CiscoIPPhoneDirectory>
'''

# Function to get the Line based on the Parking Lot
def get_line(parking_lot):
    if parking_lot == '71':
        return 'Line1'
    elif parking_lot == '72':
        return 'Line2'
    elif parking_lot == '73':
        return 'Line3'
    else:
        return parking_lot  # Default to the original parking lot number

@app.route('/parkedcalls')
def parked_calls_service():
    parked_calls = get_parked_calls()
    xml = render_template_string(xml_template, parked_calls=parked_calls, get_line=get_line)
    return Response(xml, mimetype='text/xml'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
