from flask import Flask
from flask_mqtt import Mqtt
import ast

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
custom_ip = socket.gethostbyname(socket.gethostname())
custom_port = 8080

device_info = {
    "device_name": "Slave1",
    "extra_info": "Some extra info",
    "ip": custom_ip,
    "port": custom_port,
    "RELAY_PINS": {
        1: 3,
        2: 4,
        3: 5,
        4: 6,
        5: 7,
        6: 8,
        7: 9,
        8: 10,
    },
}

RELAY_PINS = {
    1: 3,
    2: 4,
    3: 5,
    4: 6,
    5: 7,
    6: 8,
    7: 9,
    8: 10,
}

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
    print(f"Received message from {message.topic}: {payload['message']}")

@app.route('/')
def index():
    return "Slave Flask Application"

if __name__ == '__main__':
    app.run(host=custom_ip, port=custom_port, debug=True)
