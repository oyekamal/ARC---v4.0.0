# apps/device_blueprint/routes.py

from flask import render_template, request, redirect, url_for, flash
from apps import db
from apps.device.forms import DeviceForm
from apps.device.models import Device
from apps.device import blueprint

@blueprint.route('/devices', methods=['GET', 'POST'])
def devices():
    devices = Device.query.all()
    return render_template('devices/index.html', devices=devices)

@blueprint.route('/devices/add', methods=['GET', 'POST'])
def add_device():
    form = DeviceForm()
    if form.validate_on_submit():
        device = Device(
            device_ip=form.device_ip.data,
            device_name=form.device_name.data
        )
        db.session.add(device)
        db.session.commit()
        flash('Device added successfully', 'success')
        return redirect(url_for('device_blueprint.devices'))
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
