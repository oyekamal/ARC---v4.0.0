# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


from apps import db


class Device(db.Model):

    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    device_ip = db.Column(db.String(255), unique=True, nullable=False)
    device_name = db.Column(db.String(255), unique=True, nullable=False)


    def __repr__(self):
        return str(self.device_name)