
import RPi.GPIO as GPIO
import traceback
from time import sleep
from constant import CONSTANTS as C

# Set mode
GPIO.setmode(GPIO.BCM)

GPIO.setup(C["BUTTON1"], GPIO.IN)
GPIO.setup(C["BUTTON2"], GPIO.IN)
GPIO.setup(C["BUTTON4"], GPIO.IN)


GPIO.setup(C["LEFT_MOTOR_SLP"], GPIO.OUT)
GPIO.setup(C["LEFT_MOTOR_DIR"], GPIO.OUT)
GPIO.setup(C["LEFT_MOTOR_PWM"], GPIO.OUT)

GPIO.setup(C["RIGHT_MOTOR_SLP"], GPIO.OUT)
GPIO.setup(C["RIGHT_MOTOR_DIR"], GPIO.OUT)
GPIO.setup(C["RIGHT_MOTOR_PWM"], GPIO.OUT)


GPIO.setup(C["LINE_SENSOR_LED"], GPIO.OUT)
GPIO.setup(C["LINE_SENSOR_1"], GPIO.IN)
GPIO.setup(C["LINE_SENSOR_2"], GPIO.IN)
GPIO.setup(C["LINE_SENSOR_4"], GPIO.IN)
GPIO.setup(C["LINE_SENSOR_5"], GPIO.IN)
GPIO.setup(C["LINE_SENSOR_7"], GPIO.IN)
GPIO.setup(C["LINE_SENSOR_8"], GPIO.IN)

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
    r2 = GPIO.input(C["LINE_SENSOR_1"])
    r3 = GPIO.input(C["LINE_SENSOR_2"])
    r4 = GPIO.input(C["LINE_SENSOR_4"])
    r5 = GPIO.input(C["LINE_SENSOR_5"])
    r6 = GPIO.input(C["LINE_SENSOR_7"])
    r7 = GPIO.input(C["LINE_SENSOR_8"])
    GPIO.output(C["LINE_SENSOR_LED"], 0)
    sleep(2.0)
    print(r2,r3,r4,r5,r6,r7)

    # # BUTTON1 starts the motors
    # if (not GPIO.input(C["BUTTON1"])):
    #   left.start(50)
    #   right.start(50)

    #  # BUTTON3 stops the motors 
    # elif (not GPIO.input(C["BUTTON2"])):
    #   left.stop()
    #   right.stop()

     # BUTTON3 stops the motors 
    if (not GPIO.input(C["BUTTON2"])):
      print("Tset")
      GPIO.cleanup()
      exit()

  
finally:
  GPIO.cleanup()
  