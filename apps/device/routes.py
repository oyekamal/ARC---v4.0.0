# apps/device_blueprint/routes.py

from flask import render_template, request, redirect, url_for, flash
from apps import db
from apps.device.forms import DeviceForm, GroupForm
from apps.device.models import Device, Group
from apps.device import blueprint


@blueprint.route('/devices', methods=['GET', 'POST'])
def devices():
    devices = Device.query.all()
    return render_template('devices/index.html', devices=devices)


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
