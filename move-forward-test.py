
import RPi.GPIO as GPIO
import traceback
from time import sleep
from constant import CONSTANTS as C

# Set mode
GPIO.setmode(GPIO.BCM)

GPIO.setup(C["BUTTON1"], GPIO.IN)
GPIO.setup(C["BUTTON2"], GPIO.IN)

GPIO.setup(C["LEFT_MOTOR_SLP"], GPIO.OUT)
GPIO.setup(C["LEFT_MOTOR_DIR"], GPIO.OUT)
GPIO.setup(C["LEFT_MOTOR_PWM"], GPIO.OUT)

GPIO.setup(C["RIGHT_MOTOR_SLP"], GPIO.OUT)
GPIO.setup(C["RIGHT_MOTOR_DIR"], GPIO.OUT)
GPIO.setup(C["RIGHT_MOTOR_PWM"], GPIO.OUT)


GPIO.setup(C["LINE_SENSOR_LED"], GPIO.OUT)


GPIO.setup(C["LINE_SENSOR_1"], GPIO.IN)


GPIO.output(C["LEFT_MOTOR_SLP"], 0)



# control left motor
GPIO.output(C["LEFT_MOTOR_SLP"], 1)
GPIO.output(C["LEFT_MOTOR_DIR"], 0)
left = GPIO.PWM(C["LEFT_MOTOR_PWM"], 1000)

# control right motor
GPIO.output(C["RIGHT_MOTOR_SLP"], 1)
GPIO.output(C["RIGHT_MOTOR_DIR"], 0)
right = GPIO.PWM(C["RIGHT_MOTOR_PWM"], 1000)


try:
  # initially start at stop state
  left.stop()
  right.stop()

  while True:

    GPIO.output(C["LINE_SENSOR_LED"], 1)
    reading = GPIO.input(C["LINE_SENSOR_1"])
    GPIO.output(C["LINE_SENSOR_LED"], 0)
    sleep(2.0)
    print(reading)

    # BUTTON1 starts the motors
    if (not GPIO.input(C["BUTTON1"])):
      left.start(50)
      right.start(50)

     # BUTTON3 stops the motors 
    elif (not GPIO.input(C["BUTTON2"])):
      left.stop()
      right.stop()
  
finally:
  GPIO.cleanup()