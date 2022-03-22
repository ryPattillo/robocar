
import RPi.GPIO as GPIO
import traceback
from time import sleep
from constant import CONSTANTS as C

def read_line_sensor():
  '''
  Function for reading line sensor data
  TODO: figure out how to effectively do this
  '''
  time = 0

  # TODO: figure out exactly how long for capacitor to charge
  charge_time = 0.01

  # Set LED Pin to high
  GPIO.output(C["LINE_SENSOR_LED"], 1)

  # Wait for capacitor to charge
  sleep(charge_time) 

  # See how long it takes sensor to discharge to low
  while GPIO.input(C["LINE_SENSOR_4"]) > 0:
    time += 1

  # Set LED Pin back to low
  GPIO.output(C["LINE_SENSOR_LED"], 0)


  # NOTE: these are here for when we want to use more sensors
  # r2 = GPIO.input(C["LINE_SENSOR_1"])
  # r3 = GPIO.input(C["LINE_SENSOR_2"])
  # r4 = GPIO.input(C["LINE_SENSOR_4"])
  # r5 = GPIO.input(C["LINE_SENSOR_5"])
  # r6 = GPIO.input(C["LINE_SENSOR_7"])
  # r7 = GPIO.input(C["LINE_SENSOR_8"])

# Set mode
GPIO.setmode(GPIO.BCM)

# Configure Bumb Sensors
GPIO.setup(C["BUTTON1"], GPIO.IN)
GPIO.setup(C["BUTTON2"], GPIO.IN)

# Configure left motor
GPIO.setup(C["LEFT_MOTOR_SLP"], GPIO.OUT)
GPIO.setup(C["LEFT_MOTOR_DIR"], GPIO.OUT)
GPIO.setup(C["LEFT_MOTOR_PWM"], GPIO.OUT)

# Configure right motor
GPIO.setup(C["RIGHT_MOTOR_SLP"], GPIO.OUT)
GPIO.setup(C["RIGHT_MOTOR_DIR"], GPIO.OUT)
GPIO.setup(C["RIGHT_MOTOR_PWM"], GPIO.OUT)

# The led needed for the light sensors to work
GPIO.setup(C["LINE_SENSOR_LED"], GPIO.OUT)

# Allow for input from each of the sensors
GPIO.setup(C["LINE_SENSOR_1"], GPIO.IN)
GPIO.setup(C["LINE_SENSOR_2"], GPIO.IN)
GPIO.setup(C["LINE_SENSOR_4"], GPIO.IN)
GPIO.setup(C["LINE_SENSOR_5"], GPIO.IN)
GPIO.setup(C["LINE_SENSOR_7"], GPIO.IN)
GPIO.setup(C["LINE_SENSOR_8"], GPIO.IN)

# Set up left motor contrrols
GPIO.output(C["LEFT_MOTOR_SLP"], 1)
GPIO.output(C["LEFT_MOTOR_DIR"], 0)
left = GPIO.PWM(C["LEFT_MOTOR_PWM"], 1000)

# Set up right motor controls
GPIO.output(C["RIGHT_MOTOR_SLP"], 1)
GPIO.output(C["RIGHT_MOTOR_DIR"], 0)
right = GPIO.PWM(C["RIGHT_MOTOR_PWM"], 1000)

try:
  # initially start at stop state
  left.stop()
  right.stop()

  while True:

    # Get data from line sensor
    read_line_sensor()

    #BUTTON1 starts the motors
    if (not GPIO.input(C["BUTTON1"])):
      left.start(50)
      right.start(50) 

     # BUTTON2 stops the motors and ends execution
    elif (not GPIO.input(C["BUTTON2"])):
      left.stop()
      right.stop()
      GPIO.cleanup()
      exit()
except:
  print("EXCEPTION")
  
finally:
  GPIO.cleanup()
  