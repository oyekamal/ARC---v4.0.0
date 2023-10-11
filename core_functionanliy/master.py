from flask import Flask, request, jsonify
from flask_mqtt import Mqtt
import ast

app = Flask(__name__)
# app.config['MQTT_BROKER_URL'] = 'mqtt://localhost:1883'
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
# app.config['MQTT_CLEAN_SESSION'] = True
mqtt = Mqtt(app)

registered_slaves = []

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Master connected to MQTT broker")
    # Subscribe to the 'master/slaves' topic
    mqtt.subscribe('master/slaves')

@mqtt.on_message()
def handle_message(client, userdata, message):

    string = message.payload.decode('utf-8')
    payload = ast.literal_eval(string)
    print(payload['device_name'])
    if payload.get('device_name'):
        
        result = mqtt.publish(payload['device_name'], str({"message": "connected to master",}))
        if result:
            print("Message send to slave successfully")
        else:
            print("Failed to send message to slave")

#  relay_num = request.form.get('relay_num')  # Only get the relay number
#  device_ip = request.form.get('device_ip')  # Get the device IPELAY:{relay_num}")

@app.route('/toggled/', methods=['POST'])
def toggle_relay():
    relay_num = request.form.get('relay_num')  # Only get the relay number
    device_name = request.form.get('device_name')  # Get the device IP
    device_info = {
        "message": "toggle request send",
        "device_name": "Slave1",
        "extra_info": "Some extra info",
        "ip": "127.0.0.1",
        "port": "5000",
        "RELAY_PINS":{
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
    device_info['device_name'] = device_name
    device_info['relay_toggles'] = [{'relay': 2,
                                     'on_off': True}]
    result = mqtt.publish(device_name, str(device_info))
    return jsonify(success=True, message="Toggle command sent!")

@app.route('/')
def index():
    return "Master Flask Application"

if __name__ == '__main__':
    app.run(debug=True)
