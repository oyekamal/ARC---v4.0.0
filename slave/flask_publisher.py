from flask import Flask, request
import paho.mqtt.client as mqtt

app = Flask(__name__)

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)  # connect to broker
    client.publish("flask/mqtt", message)  # publish message
    return "Message Published!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
