
import RPi.GPIO as GPIO
import traceback
from time import sleep

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.IN)
GPIO.setup(3, GPIO.IN)

GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

GPIO.output(10, 1)
GPIO.output(9, 0)
left = GPIO.PWM(11, 1000)

GPIO.output(5, 1)
GPIO.output(6, 0)
right = GPIO.PWM(13, 1000)


try:
  left.stop()
  right.stop()

  while True:
    if (not GPIO.input(2)):
      left.start(50)
      right.start(50)
    elif (not GPIO.input(3)):
      left.stop()
      right.stop()

except:
  traceback.print_exc()
  
finally:
  GPIO.cleanup()