import serial
import time
from inputs import get_gamepad


# Configurar la comunicación serie con el Arduino
arduino_tx = '/dev/ttyS0'  # Puerto TX en Raspberry Pi (puede variar según el modelo)
arduino_baud = 9600
ser = serial.Serial(arduino_tx, arduino_baud, timeout=1)

# Función para enviar los ángulos al Arduino
def enviar_angulos(angulo_servo1, angulo_servo2):
    ser.write(f"{angulo_servo1},{angulo_servo2}\n".encode())

# Rango de movimiento de los servomotores
servo1_min_angle = 0
servo1_max_angle = 180 #joyIzquierdo
servo2_min_angle = 0
servo2_max_angle = 180 #joyDerecho

# Mapear el valor del eje Y del control de Xbox al rango de los servomotores
def map_value(value, from_low, from_high, to_low, to_high):
    return int((value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low)

try:
    while True:
        events = get_gamepad()
        for event in events:
            # Joystick izquierdo controla el primer servomotor
            if event.ev_type == 'Absolute' and event.code == 'ABS_Y':
                angle_y_servo1 = map_value(event.state, -32768, 32767, servo1_min_angle, servo1_max_angle)
            
            # Joystick derecho controla el segundo servomotor
            if event.ev_type == 'Absolute' and event.code == 'ABS_RY':
                angle_y_servo2 = map_value(event.state, -32768, 32767, servo2_min_angle, servo2_max_angle)
                
                # Enviar los ángulos al Arduino
                enviar_angulos(angle_y_servo1, angle_y_servo2)
                print(f"Enviando ángulos: Servo1={angle_y_servo1}, Servo2={angle_y_servo2}") 

        # Pequeño retardo para evitar lecturas rápidas del controlador
        time.sleep(0.01)

except KeyboardInterrupt:
    pass

# Cerrar la conexión serial
ser.close()
