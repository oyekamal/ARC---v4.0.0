from flask import Flask
import paho.mqtt.client as mqtt
# please add what you want to send to the master from slave in form of {}
app = Flask(__name__)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("rayan")

def on_message(client, userdata, msg):
    print(msg.payload)
    print("Received message: "+str(msg.payload.decode()))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_start()

@app.route('/')
def index():
    return "Listening for messages!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
