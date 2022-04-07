import RPi.GPIO as GPIO
from time import sleep
from constant import CONSTANTS as C
from pin_setup import setup
import keyboard
# setup()
# left =  GPIO.PWM(C["LEFT_MOTOR_PWM"], 1000)
# right = GPIO.PWM(C["RIGHT_MOTOR_PWM"], 1000)


def key_press(key):

  print(key.name)
  # if key.name == "left":
  #   return(key.name)
  #   pass

  # elif key == "right":
  #   # turn right
  #   pass

  # elif key == "up":
  #   # speed up
  #   pass 
 
  # elif key == "down":
  #   # slow down
  #   pass

if __name__ == "__main__":
  
  keyboard.on_press(key_press)

  while True:

    pass
  
