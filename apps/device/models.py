# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


from apps import db
from sqlalchemy.orm import relationship

class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), unique=True, nullable=False)
    is_on = db.Column(db.Boolean, default=False)

    # Define the many-to-many relationship with Device
    devices = relationship('Device', secondary='group_device_association', back_populates='groups')

    def __repr__(self):
        return str(self.group_name)


group_device_association = db.Table(
    'group_device_association',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('device_id', db.Integer, db.ForeignKey('device.id'))
)


class Relay(db.Model):
    __tablename__ = 'relay'

    id = db.Column(db.Integer, primary_key=True)
    relay_pin = db.Column(db.Integer, nullable=False)
    is_on = db.Column(db.Boolean, default=False)
    relay_name = db.Column(db.String(255), nullable=True)
    # Define a foreign key relationship to the Device table
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    device = db.relationship('Device', back_populates='relays')

        # Add a many-to-many relationship with RelayGroup
    relay_groups = db.relationship('RelayGroup', secondary='relay_group_relay_association', back_populates='relays')

    def __repr__(self):
        return f"Relay {self.relay_number} for Device {self.device_id}"

class Device(db.Model):

    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    device_ip = db.Column(db.String(255), nullable=True)
    device_name = db.Column(db.String(255), nullable=True)
    extra = db.Column(db.JSON, nullable=True)
    is_on = db.Column(db.Boolean, default=False)

    # Define the one-to-many relationship with Relay
    relays = db.relationship('Relay', back_populates='device')

    # Define the many-to-many relationship back-reference to Group
    groups = relationship('Group', secondary='group_device_association', back_populates='devices')


    def __repr__(self):
        return str(self.device_name)
    

class RelayGroup(db.Model):
    __tablename__ = 'relay_group'

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), unique=True, nullable=False)
    is_on = db.Column(db.Boolean, default=True)

    # Define the many-to-many relationship with Relay
    relays = db.relationship('Relay', secondary='relay_group_relay_association', back_populates='relay_groups')

    def __repr__(self):
        return str(self.group_name)

relay_group_relay_association = db.Table(
    'relay_group_relay_association',
    db.Column('relay_group_id', db.Integer, db.ForeignKey('relay_group.id')),
    db.Column('relay_id', db.Integer, db.ForeignKey('relay.id'))
)



