
import paho.mqtt.client as mqtt
import json

def publisher(topic_name, data):
    # Publish the status update to the MQTT topic
    mqtt_client = mqtt.Client()
    mqtt_client.connect("localhost", 1883, 60)
    # topic = f"flask/mqtt/{topic_name}"
    message = {"data": data}
    mqtt_client.publish(topic_name, json.dumps(message))
    print("sended successfully")