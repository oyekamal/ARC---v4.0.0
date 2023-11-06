import RPi.GPIO as GPIO
import time

# Set the GPIO pin number
pin = 3

# Set up the GPIO mode and pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

# Toggle the GPIO pin
GPIO.output(pin, GPIO.HIGH)
print("Pin set to HIGH")
time.sleep(0.8)
GPIO.output(pin, GPIO.LOW)
print("Pin set to LOW")

# Clean up the GPIO
GPIO.cleanup()
