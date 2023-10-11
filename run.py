# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit

from apps.config import config_dict
from apps import create_app, db
from apps import mqtt
import ast

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)


print("mqtt is available")

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Master connected to MQTT broker")
    # Subscribe to the 'master/slaves' topic
    mqtt.subscribe('master/slaves')

@mqtt.on_message()
def handle_message(client, userdata, message):

    string = message.payload.decode('utf-8')
    payload = ast.literal_eval(string)
    print(payload)
    with app.app_context():
        from apps.device.models import Device, Group, Relay
        d = Device.query.all()
    if payload.get('device_name'):
        result = mqtt.publish(payload['device_name'], str({"message": "connected to master"}))
        if result:
            print("Message sent to slave successfully")
        else:
            print("Failed to send message to slave")

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)
    
if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)

if __name__ == "__main__":
    app.run()
