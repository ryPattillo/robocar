
import RPi.GPIO as GPIO
from time import sleep
from constant import CONSTANTS as C
from pin_configure import configure

def not_defined():
    print("BUTTON HAS NO FUNCTIOALITY")

def start_motors():
    GPIO.PWM(C["LEFT_MOTOR_PWM"], 1000).start(50)
    GPIO.PWM(C["RIGHT_MOTOR_PWM"], 1000).start(50)

def stop_motors():
    GPIO.PWM(C["LEFT_MOTOR_PWM"], 1000).stop()
    GPIO.PWM(C["RIGHT_MOTOR_PWM"], 1000).stop()

def end():
    GPIO.cleanup()
    exit()

if __name__ == "__main__":
  configure()

  # Set up left motor contorls
  GPIO.output(C["LEFT_MOTOR_SLP"], 1)
  GPIO.output(C["LEFT_MOTOR_DIR"], 0)
  # Set up right motor controls
  GPIO.output(C["RIGHT_MOTOR_SLP"], 1)
  GPIO.output(C["RIGHT_MOTOR_DIR"], 0)

  print("BUTTON 1 STARTS MOTORS")
  print("BUTTON 2 STOPS MOTORS")
  print("BUTTON 3 ENDS EXECUTION")
  GPIO.add_event_detect(C["BUTTON1"],GPIO.FALLING, callback = start_motors,bouncetime = 200)
  GPIO.add_event_detect(C["BUTTON2"],GPIO.FALLING, callback = stop_motors,bouncetime = 200)
  GPIO.add_event_detect(C["BUTTON3"],GPIO.FALLING, callback = end,bouncetime = 200)
  GPIO.add_event_detect(C["BUTTON4"],GPIO.FALLING, callback = not_defined,bouncetime = 200)
  GPIO.add_event_detect(C["BUTTON5"],GPIO.FALLING, callback = not_defined,bouncetime = 200)
  GPIO.add_event_detect(C["BUTTON6"],GPIO.FALLING, callback = not_defined,bouncetime = 200)

      # Set up left motor contrrols

  while True:
    pass
    # NOTE: This will be where we are getting camera data
  