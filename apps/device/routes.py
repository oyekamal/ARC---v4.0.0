# apps/device_blueprint/routes.py

from flask import render_template, request, redirect, url_for, flash
from apps import db
from apps.device.forms import DeviceForm, GroupForm
from apps.device.models import Device, Group, Relay, RelayGroup
from apps.device import blueprint
from apps import mqtt
import ast
from apps.device.mqtt_routes import send_request_to_device


@blueprint.route('/devices', methods=['GET', 'POST'])
def devices():
    devices = Device.query.all()
    return render_template('devices/index.html', devices=devices)


@blueprint.route('/update_device_status/<int:id>', methods=['POST'])
def update_device_status(id):
    device = Device.query.get_or_404(id)
    
    if request.method == 'POST':
        new_status = int(request.form.get('is_on', 0))
        device.is_on = bool(new_status)
        db.session.commit()
        print(device.device_name)
        # publisher(device.device_name, "hello world")
    
    return redirect(url_for('device_blueprint.devices'))

@blueprint.route('/update_group/<int:group_id>', methods=['POST'])
def update_group(group_id):
    group = Group.query.get_or_404(group_id)
    
    if request.method == 'POST':
        new_status = int(request.form.get('is_on', 0))
        group.is_on = bool(new_status)
        print(group)
        for device in group.devices:
            device.is_on = bool(new_status)
            publisher(device.device_name, "hello world")
        db.session.commit()

    return redirect(url_for('device_blueprint.groups'))

@blueprint.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    form = DeviceForm()
    if form.validate_on_submit():
        try:
            # Check if the device_ip or device_name already exist in the database
            existing_device = Device.query.filter(
                (Device.device_ip == form.device_ip.data) |
                (Device.device_name == form.device_name.data)
            ).first()

            if existing_device:
                flash('Device with the same IP or Name already exists', 'error')
            else:
                device = Device(
                    device_ip=form.device_ip.data,
                    device_name=form.device_name.data
                )
                db.session.add(device)
                db.session.commit()
                flash('Device added successfully', 'success')
                return redirect(url_for('device_blueprint.devices'))
        except Exception as e:
            db.session.rollback()  # Rollback the session in case of an error
            flash('An error occurred while adding the device', 'error')
            print(str(e))  # Print the error for debugging
    return render_template('devices/add.html', form=form)


@blueprint.route('/devices/edit/<int:id>', methods=['GET', 'POST'])
def edit_device(id):
    device = Device.query.get(id)
    form = DeviceForm(obj=device)
    if form.validate_on_submit():
        device.device_ip = form.device_ip.data
        device.device_name = form.device_name.data
        db.session.commit()
        flash('Device updated successfully', 'success')
        return redirect(url_for('device_blueprint.devices'))
    return render_template('devices/edit.html', form=form, device=device)


@blueprint.route('/devices/delete/<int:id>', methods=['POST'])
def delete_device(id):
    device = Device.query.get(id)
    db.session.delete(device)
    db.session.commit()
    flash('Device deleted successfully', 'success')
    return redirect(url_for('device_blueprint.devices'))


@blueprint.route('/groups', methods=['GET', 'POST'])
def groups():
    groups = Group.query.all()
    group_form = GroupForm()  # Create an instance of the GroupForm
    return render_template('groups/index.html', groups=groups, group_form=group_form)


@blueprint.route('/groups/add', methods=['GET', 'POST'])
def add_group():
    # groups = Group.query.all()
    group_form = GroupForm()
    if group_form.validate_on_submit():
        try:
            existing_group = Group.query.filter_by(
                group_name=group_form.group_name.data).first()
            if existing_group:
                flash('Group with the same name already exists', 'error')
            else:
                group = Group(group_name=group_form.group_name.data)
                db.session.add(group)
                db.session.commit()
                flash('Group added successfully', 'success')
                return redirect(url_for('device_blueprint.groups'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the group', 'error')
            print(str(e))
    return render_template('groups/index.html', group_form=group_form)


@blueprint.route('/groups/edit/<int:id>', methods=['GET', 'POST'])
def edit_group(id):
    group = Group.query.get(id)
    group_form = GroupForm(obj=group)
    if group_form.validate_on_submit():
        try:
            existing_group = Group.query.filter(
                Group.id != id, Group.group_name == group_form.group_name.data).first()
            if existing_group:
                flash('Group with the same name already exists', 'error')
            else:
                group.group_name = group_form.group_name.data
                db.session.commit()
                flash('Group updated successfully', 'success')
                return redirect(url_for('device_blueprint.groups'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the group', 'error')
            print(str(e))
    return render_template('groups/edit.html', group=group, group_form=group_form)



@blueprint.route('/groups/delete/<int:id>', methods=['POST'])
def delete_group(id):
    group = Group.query.get(id)
    try:
        db.session.delete(group)
        db.session.commit()
        flash('Group deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the group', 'error')
        print(str(e))
    return redirect(url_for('device_blueprint.groups'))


@blueprint.route('/groups/<int:group_id>/devices', methods=['GET', 'POST'])
def add_or_remove_devices_from_group(group_id):
    group = Group.query.get(group_id)
    group_form = GroupForm(obj=group)

    available_devices = Device.query.all()
    selected_device_ids = [device.id for device in group.devices]

    if request.method == 'POST':
        selected_device_ids = request.form.getlist('device_ids[]')  # Get a list of selected device IDs from the form

        # Clear the group's devices to start with an empty list
        group.devices = []

        # Iterate over the available devices and add them to the group if they are in the selected IDs
        for device in available_devices:
            if str(device.id) in selected_device_ids:
                group.devices.append(device)

        db.session.commit()
        flash('Devices in the group have been updated successfully', 'success')
        # return render_template('groups/edit_group_devices.html', group=group, available_devices=available_devices, group_form=group_form, selected_device_ids=selected_device_ids)
        return redirect(url_for('device_blueprint.groups'))
    return render_template('groups/edit_group_devices.html', group=group, available_devices=available_devices, group_form=group_form, selected_device_ids=selected_device_ids)



@blueprint.route('/device_relays/<int:device_id>')
def device_relays(device_id):
    device = Device.query.get(device_id)
    return render_template('devices/device_relays.html', device=device)



@blueprint.route('/update_relay_status/<int:id>', methods=['POST'])
def update_relay_status(id):
    relay = Relay.query.get(id)
    if relay:
        is_on = request.form.get('is_on') == '1'  # Check the value of the radio button
        relay.is_on = is_on
        db.session.commit()
        send_request_to_device(device_name=relay.device.device_name, relay=relay)
    return redirect(url_for('device_blueprint.device_relays', device_id=relay.device_id))

@blueprint.route('/edit_relay/<int:id>', methods=['GET', 'POST'])
def edit_relay(id):
    relay = Relay.query.get(id)

    if request.method == 'POST':
        is_on = request.form.get('is_on') == '1'
        relay.is_on = is_on
        relay.relay_name = request.form.get('relay_name')  # Update relay_name
        db.session.commit()
        send_request_to_device(device_name=relay.device.device_name, relay=relay)
        return redirect(url_for('device_blueprint.device_relays', device_id=relay.device_id))
    return render_template('devices/edit_relay.html', relay=relay)


# CRUD operations for RelayGroup
@blueprint.route('/relay_groups', methods=['GET'])
def list_relay_groups():
    relay_groups = RelayGroup.query.all()
    return render_template('devices/relay_groups.html', relay_groups=relay_groups)

@blueprint.route('/relay_groups/add_relay_group', methods=['GET', 'POST'])
def add_relay_group():
    if request.method == 'POST':
        group_name = request.form['group_name']
        is_on = request.form.get('is_on') == 'on'

        # Create a new RelayGroup
        new_group = RelayGroup(group_name=group_name, is_on=is_on)
        db.session.add(new_group)
        db.session.commit()

        return redirect(url_for('device_blueprint.list_relay_groups'))
    
    return render_template('devices/add_relay_group.html')

@blueprint.route('/relay_groups/add_relay/<int:relay_group_id>', methods=['POST'])
def add_relay_to_group(relay_group_id):
    relay_group = RelayGroup.query.get(relay_group_id)
    relay_id = request.form.get('relay_id')  # Assuming you have a form field for relay selection
    relay = Relay.query.get(relay_id)
    
    if relay and relay_group:
        relay_group.relays.append(relay)
        db.session.commit()
    
    return redirect(url_for('device_blueprint.list_relay_groups'))

@blueprint.route('/relay_groups/remove_relay/<int:relay_group_id>', methods=['POST'])
def remove_relay_from_group(relay_group_id):
    relay_group = RelayGroup.query.get(relay_group_id)
    relay_id = request.form.get('relay_id')  # Assuming you have a form field for relay selection
    relay = Relay.query.get(relay_id)
    
    if relay and relay_group:
        relay_group.relays.remove(relay)
        db.session.commit()
    
    return redirect(url_for('device_blueprint.list_relay_groups'))

@blueprint.route('/relay_groups/edit/<int:relay_group_id>', methods=['GET', 'POST'])
def edit_relay_group(relay_group_id):
    relay_group = RelayGroup.query.get(relay_group_id)
    
    if request.method == 'POST':
        new_group_name = request.form['group_name']
        is_on = request.form.get('is_on') == 'on'
        
        if relay_group:
            relay_group.group_name = new_group_name
            relay_group.is_on = is_on
            db.session.commit()
    
    return render_template('devices/edit_relay_group.html', relay_group=relay_group)

@blueprint.route('/relay_groups/delete/<int:relay_group_id>', methods=['POST'])
def delete_relay_group(relay_group_id):
    relay_group = RelayGroup.query.get(relay_group_id)
    
    if relay_group:
        db.session.delete(relay_group)
        db.session.commit()
    
    return redirect(url_for('device_blueprint.list_relay_groups'))
# print("mqtt is available")

# @mqtt.on_connect()
# def handle_connect(client, userdata, flags, rc):
#     print("Master connected to MQTT broker")
#     # Subscribe to the 'master/slaves' topic
#     mqtt.subscribe('master/slaves')

# @mqtt.on_message()
# def handle_message(client, userdata, message):
#     string = message.payload.decode('utf-8')
#     payload = ast.literal_eval(string)
#     print(payload)
#     if payload.get('device_name'):
#         result = mqtt.publish(payload['device_name'], str({"message": "connected to master"}))
#         if result:
#             print("Message sent to slave successfully")
#         else:
#             print("Failed to send message to slave")