import RPi.GPIO as GPIO
from gpiozero import Servo
import serial
import time
from inputs import get_gamepad

# Configure serial communication with Arduino
arduino_tx = '/dev/ttyS0'  # TX port on Raspberry Pi (may vary depending on the model)
arduino_baud = 9600
ser = serial.Serial(arduino_tx, arduino_baud, timeout=1)

# Function to send angles to Arduino
def send_angles(servo1_angle, servo2_angle):
    ser.write(f"{servo1_angle},{servo2_angle}\n".encode())

# Servo motors' range of movement
servo_min_angle = 0
servo_max_angle = 180

# Map Xbox controller's Y-axis value to servo motors' range
def map_value(value, from_low, from_high, to_low, to_high):
    return int((value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low)

try:
    while True:
        events = get_gamepad()
        for event in events:
            # Left joystick controls both servo motors (forward and backward)
            if event.ev_type == 'Absolute' and event.code == 'ABS_Y':
                angle = map_value(event.state, -32768, 32767, servo_max_angle, servo_min_angle)
                
                # Send angles to Arduino for both servo motors
                send_angles(angle, servo_max_angle - angle)  # Invert angle for the second servo motor
                print(f"Sending angles: Servo1={angle}, Servo2={servo_max_angle - angle}") 
            
            # Right joystick controls the second servo motor (left and right)
            if event.ev_type == 'Absolute' and event.code == 'ABS_RX':
                angle_x = map_value(event.state, -32768, 32767, servo_min_angle, servo_max_angle)
                
                # Send angle to Arduino only for the second servo motor
                send_angles(angle, angle_x)
                print(f"Sending angles: Servo1={angle}, Servo2={angle_x}") 

        # Small delay to prevent rapid controller readings
        time.sleep(0.01)

except KeyboardInterrupt:
    pass

# Close serial connection
ser.close()
