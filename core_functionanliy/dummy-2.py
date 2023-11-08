from flask import Flask
from flask_mqtt import Mqtt
import ast
import platform
import time

import RPi.GPIO as GPIO
import socket
from threading import Thread

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)

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
custom_ip = '127.0.0.12'
custom_port = 8082

# Define the relay pins to monitor
relay_pins_to_monitor = [3, 4, 5]

# Initialize GPIO for relay pins
for pin in relay_pins_to_monitor:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

device_info = {
    "device_type": "dummy",
    "device_name": "Dummy-16R-3-Relayworking",
    "extra_info": "Some extra info",
    "ip": custom_ip,
    "port": custom_port,
    "RELAY_PINS": {
        1: 3,
        2: 4,
        2: 5,
    },
    "relay_on_off": [{3:False}],
    "message": "hello Master",
    "device_update": False,
}
def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    for relay_num, pin in device_info["RELAY_PINS"].items():
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Slave connected to MQTT broker")
    mqtt.subscribe(device_info['device_name'])
    result = mqtt.publish('master/slaves', str(device_info))
    if result:
        print("Message published successfully")
    else:
        print("Failed to publish message")

def send_notification(device_info):
    result = mqtt.publish('master/slaves', str(device_info))
    if result:
        print("Notification sent successfully")
    else:
        print("Failed to send notification")

def listen_to_relay_changes():
    while True:
        # for relay_pin in relay_pins_to_monitor:
        #     current_state = GPIO.input(relay_pin)
        #     for key, value in device_info['relay_on_off'].items(): #[{3:True},{4:False},{5:False},]
        #         if relay_pin == key:
        #             if current_state != value:
        #                 for each_dict in device_info['relay_on_off']:
        #                     if each_dict.get(relay_pin):
        #                         each_dict[relay_pin] = current_state
        #                 send_notification(device_info)


        current_state = GPIO.input(3)
        three = device_info['relay_on_off'][0]
        print(three)
        print(type(three))
        value = three[3]
        print('   current_state --->   ',current_state)
        if current_state != value:
            three[3] = current_state
            # send_notification(device_info)
        time.sleep(1)  # Adjust the interval as needed

@mqtt.on_message()
def handle_message(client, userdata, message):
    string = message.payload.decode('utf-8')
    payload = ast.literal_eval(string)
    print(payload)
    if payload['device_update'] and payload['relay_on_off']:
        print(payload['relay_on_off'])
        for relay_pin, state in payload['relay_on_off'].items():
            GPIO.setup(relay_pin, GPIO.OUT)
            GPIO.output(relay_pin, state)
            time.sleep(0.8)
            GPIO.output(relay_pin, GPIO.LOW)
    print(f"Received message from {message.topic}: {payload['message']}")

@app.route('/')
def index():
    return "Slave Flask Application"

if __name__ == '__main__':
    device_info['relay_on_off'] = [{pin:bool(GPIO.input(pin))} for pin in relay_pins_to_monitor]
    initialize_gpio()
    listen_to_relay_changes_thread = Thread(target=listen_to_relay_changes)
    listen_to_relay_changes_thread.start()
    app.run(host=custom_ip, port=custom_port, debug=True)
