import RPi.GPIO as GPIO
from time import sleep
from constant import CONSTANTS as C
from pin_setup import setup
import keyboard
# setup()
# left =  GPIO.PWM(C["LEFT_MOTOR_PWM"], 1000)
# right = GPIO.PWM(C["RIGHT_MOTOR_PWM"], 1000)

def key_press(key):
  print("Key: ", key.name)


if __name__ == "__main__":

  # set up all the pin

  # Collect events until released
  # with keyboard.Listener(
  #       on_press=on_press,
  #       on_release=on_release) as listener:
  #   listener.join()

  keyboard.on_press(key_press)
  while True:

    pass
    # Capture an image every 2 seconds
    # sleep(2)
    #camera.capture('foo.jpg')
  
    # find_sign('image.jp')
    # if sign == 'speed_up':
        # speed up
    # elif sign == 'slow_down: 
      # slow down
