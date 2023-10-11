 # if 'device_name' in payload and 'ip' in payload:
    #     device_name = payload['device_name']
    #     device_ip = payload['ip']

    #     # Check if the device already exists in the database
    #     existing_device = Device.query.filter_by(device_name=device_name, device_ip=device_ip).first()

    #     if existing_device:
    #         # Update the existing device's information
    #         existing_device.is_on = True  # Update as needed
    #         existing_device.extra = payload.get('extra')  # Update extra info as needed

    #         # Update or create relays
    #         if 'RELAY_PINS' in payload:
    #             for relay_number, relay_pin in payload['RELAY_PINS'].items():
    #                 relay = Relay.query.filter_by(device_id=existing_device.id, relay_pin=relay_pin).first()
    #                 if relay:
    #                     relay.is_on = True  # Update as needed
    #                     relay.relay_name = f"Relay {relay_number}"  # Update as needed
    #                 else:
    #                     new_relay = Relay(
    #                         relay_pin=relay_pin,
    #                         is_on=True,  # Update as needed
    #                         relay_name=f"Relay {relay_number}",  # Update as needed
    #                         device=existing_device
    #                     )
    #                     db.session.add(new_relay)

    #     else:
    #         # Create a new device entry
    #         new_device = Device(
    #             device_name=device_name,
    #             device_ip=device_ip,
    #             is_on=True,  # Update as needed
    #             extra=payload.get('extra')  # Update extra info as needed
    #         )
    #         db.session.add(new_device)

    #         # Create relays for the new device
    #         if 'RELAY_PINS' in payload:
    #             for relay_number, relay_pin in payload['RELAY_PINS'].items():
    #                 new_relay = Relay(
    #                     relay_pin=relay_pin,
    #                     is_on=True,  # Update as needed
    #                     relay_name=f"Relay {relay_number}",  # Update as needed
    #                     device=new_device
    #                 )
    #                 db.session.add(new_relay)

    #     db.session.commit()
