from flask import Flask
from flask_mqtt import Mqtt
import ast
import RPi.GPIO as GPIO

app = Flask(__name__)
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
mqtt = Mqtt(app)

# Define the IP and port you want the app to run on
import socket
custom_ip = '127.0.0.12'
custom_port = 8080

device_info = {
    "device_name": "TD-16R-2-open",
    "extra_info": "Some extra info",
    "ip": custom_ip,
    "port": custom_port,
    "RELAY_PINS": {
        1: 3,
        2: 4,
    },
    "relay_on_off": [],
    "message": "hello Master",
    "device_update": False,
}

# def update_relay_json(relays):
#     relay_on_off_list = []
#     for each_relay in relays:
#         relay_on_off_list.append({each_relay.relay_pin: each_relay.is_on})
#     return relay_on_off_list

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Slave connected to MQTT broker")
    mqtt.subscribe(device_info['device_name'])
    result = mqtt.publish('master/slaves', str(device_info))
    if result:
        print("Message published successfully")
    else:
        print("Failed to publish message")

@mqtt.on_message()
def handle_message(client, userdata, message):
    print("Message", message)

    string = message.payload.decode('utf-8')
    payload = ast.literal_eval(string)

    print(payload)
    if payload['device_update'] and payload['relay_on_off']:
        print(payload['relay_on_off'])
        for each_relay in payload['relay_on_off']:
            for key, value in each_relay.items():
                if value:
                    GPIO.output(key, GPIO.HIGH)
                else:
                    GPIO.output(key, GPIO.LOW)

        # logic for toggling device
    print(f"Received message from {message.topic}: {payload['message']}")

@app.route('/')
def index():
    return "Slave Flask Application"

if __name__ == '__main__':
    app.run(host=custom_ip, port=custom_port, debug=True)
