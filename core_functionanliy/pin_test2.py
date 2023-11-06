import RPi.GPIO as GPIO
import time

sensorPin = 34  # Analog input pin connected to the sensor
outputPin = 15  # Digital output pin D15 connected to the Raspberry Pi

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(outputPin, GPIO.OUT)

def loop():
    sensorValue = analog_read(sensorPin)  # Read the analog voltage from the sensor
    voltage = sensorValue * (3.3 / 4095.0)  # Convert the ADC reading to voltage (assuming a 3.3V reference voltage)

    print("Sensor Value: ", sensorValue)  # Print the raw sensor value
    print("Voltage: ", voltage)  # Print the calculated voltage

    if voltage > 3.0:
        GPIO.output(outputPin, GPIO.HIGH)  # If voltage is greater than 3.0V, set output pin HIGH (Motion active)
        print("Motion Active")
    else:
        GPIO.output(outputPin, GPIO.LOW)  # If voltage is 3.0V or less, set output pin LOW (Zone empty)
        print("Zone Empty")

    time.sleep(1)  # Delay to avoid excessive output (adjust as needed)

def analog_read(pin):
    GPIO.setup(pin, GPIO.IN)
    adc_value = 0
    for _ in range(10):
        adc_value += GPIO.input(pin)
    adc_value /= 10
    return int(adc_value)

if __name__ == '__main__':
    setup()
    try:
        while True:
            loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
