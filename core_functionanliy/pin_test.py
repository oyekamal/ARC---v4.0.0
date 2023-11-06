import RPi.GPIO as GPIO

# Set the mode to use the BCM numbering scheme
GPIO.setmode(GPIO.BCM)

# Define the pins to check
pins_to_check = [3, 4]

# Initialize the GPIO pins
for pin in pins_to_check:
    GPIO.setup(pin, GPIO.IN)

# Function to check the status of the pins
def check_pins():
    pin_status = {}
    for pin in pins_to_check:
        pin_status[pin] = GPIO.input(pin)
    return pin_status

# Check the pins and print the status
pin_status = check_pins()
print(pin_status)
