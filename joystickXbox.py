from gpiozero import Servo
from inputs import get_gamepad
import serial
import RPi.GPIO as GPIO
import time


arduino_tx = '/dev/ttyS0'  # TX Port on Raspberry Pi
arduino_rx = '/dev/ttyS1'  # RX Port on Raspberry Pi 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

arduino_baud = 9600
ser = serial.Serial(arduino_tx, arduino_baud, timeout=1)

# Function to send the angle to Arduino
def send_angle(angle):
    ser.write(f"{angle}\n".encode())

# Servomotor movement range
servo_min_angle = 0
servo_max_angle = 180

# Map Xbox controller's Y-axis value to the servomotor range
def map_value(value, from_low, from_high, to_low, to_high):
    return int((value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low)

try:
    while True:
        events = get_gamepad()
        for event in events:
            # The Xbox controller reports events for the left joystick on axes 'ABS_X' and 'ABS_Y'
            if event.ev_type == 'Absolute' and event.code == 'ABS_Y':
                # Map the Y-axis value to the servomotor's movement range
                angle_y = map_value(event.state, -32768, 32767, servo_min_angle, servo_max_angle)
                
                # Send the angle to Arduino
                send_angle(angle_y)
                print(f"Sending angle: {angle_y}")

        # Small delay to prevent rapid controller readings
        time.sleep(0.01)

except KeyboardInterrupt:
    pass

# Close the serial connection
ser.close()