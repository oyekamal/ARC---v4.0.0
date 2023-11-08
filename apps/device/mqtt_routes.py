from apps import db
from apps.device.models import Device, Group, Relay
from apps.device.utils import DEVICE_JSON
from flask_mqtt import Mqtt
from apps import mqtt


def update_relay_json(relays):
    relay_on_off_list = []
    for each_relay in relays:
        relay_on_off_list.append({each_relay.relay_pin: each_relay.is_on})
    return relay_on_off_list


def send_request_to_device(device_name, relay,
                           data=DEVICE_JSON):
    data['relay_on_off'] = update_relay_json(relay)
    data['device_name'] = device_name
    data['device_update'] = True
    data['message'] = "Update relay"
    result = mqtt.publish(device_name, str(data))
    if result:
        print("Message Send Request to Device.")
    else:
        print("Failed to Send Request to Device")


def send_request_to_group_relay(relay, is_on=None):
    print(relay)
    if relay.relay_relay_group_associations:
        for each_group in relay.relay_relay_group_associations:
            if each_group.relay_group:
                for relay in each_group.relay_group.relays:
                    if is_on != None:
                        relay.is_on = is_on
                    send_request_to_device(device_name=relay.device.device_name, relay=[relay])


def update_create_device(payload):
    if 'device_name' in payload and 'ip' in payload:
        device_name = payload['device_name']
        device_ip = payload['ip']

        # Check if the device already exists in the database
        existing_device = Device.query.filter_by(
            device_name=device_name, device_ip=device_ip).first()

        if existing_device:
            # Update the existing device's information
            existing_device.is_on = True  # Update as needed
            existing_device.extra = payload.get(
                'extra_info')  # Update extra info as needed
            existing_device.device_type = payload.get(
                'device_type')  # Update extra info as needed

            # Update or create relays
            if 'RELAY_PINS' in payload:
                for relay_number, relay_pin in payload['RELAY_PINS'].items():
                    relay = Relay.query.filter_by(
                        device_id=existing_device.id, relay_pin=relay_pin).first()
                    if relay:
                        relay.is_on = True  # Update as needed
                        # Update as needed
                        # relay.relay_name = f"Relay {relay_number}"
                    else:
                        new_relay = Relay(
                            relay_pin=relay_pin,
                            is_on=True,  # Update as needed
                            # Update as needed
                            relay_name=f"Relay {relay_number}",
                            device=existing_device
                        )
                        db.session.add(new_relay)

        else:
            # Create a new device entry
            new_device = Device(
                device_name=device_name,
                device_ip=device_ip,
                is_on=True,  # Update as needed
                extra=payload.get('extra_info'),  # Update extra info as needed
                device_type=payload.get(
                'device_type')
            )
            db.session.add(new_device)

            # Create relays for the new device
            if 'RELAY_PINS' in payload:
                for relay_number, relay_pin in payload['RELAY_PINS'].items():
                    new_relay = Relay(
                        relay_pin=relay_pin,
                        is_on=True,  # Update as needed
                        relay_name=f"Relay {relay_number}",  # Update as needed
                        device=new_device
                    )
                    db.session.add(new_relay)

        db.session.commit()
    elif "device_name" in payload and "device_name" in payload:
        device_name = payload['device_name']
        existing_device = Device.query.filter_by(
            device_name=device_name).first()

        if existing_device:
            if 'relay_on_off' in payload:
                for relay in payload['relay_on_off']:
                    for relay_pin, value in relay.items():
                        relay = Relay.query.filter_by(
                            device_id=existing_device.id, relay_pin=relay_pin).first()
                        relay.is_on = value
                        send_request_to_group_relay(relay, value)
                        db.session.commit()


            
