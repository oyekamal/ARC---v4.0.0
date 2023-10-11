
from apps import mqtt
import ast

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
    print(payload['device_name'])
    if payload.get('device_name'):
        result = mqtt.publish(payload['device_name'], str({"message": "connected to master",}))
        if result:
            print("Message sent to slave successfully")
        else:
            print("Failed to send message to slave")