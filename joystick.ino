#include <Servo.h>

Servo servo1;
Servo servo2;
String inputString = "";  // String to store received data

void setup() {
  Serial.begin(9600); 
  servo1.attach(9);   
  servo2.attach(10);  
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    
    if (c == '\n') { // Newline character found, process angles
      int angleServo1, angleServo2;
      sscanf(inputString.c_str(), "%d,%d", &angleServo1, &angleServo2);
      inputString = ""; // Reset the string for the next command
      
      // Limit angles to servo limits (0 to 180 degrees)
      angleServo1 = constrain(angleServo1, 0, 180);
      angleServo2 = constrain(angleServo2, 0, 180);
      
      // Move the servos to the positions received via serial port
      servo1.write(angleServo1);
      servo2.write(angleServo2);
    } else {
      inputString += c; // Add the character to the string
    }
  }
}
