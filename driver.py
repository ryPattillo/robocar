
import RPi.GPIO as GPIO
from time import sleep
from constant import CONSTANTS as C
from pin_configure import setup
from picamera import PiCamera

def not_defined(channel):
    '''
    Callback that does nothing
    '''
    print("BUTTON HAS NO FUNCTIOALITY")

def start_motors(channel):
    '''
    Call back to start the motors
    '''

    # NOTE: The motors are not being start up for some reason
    print("MOTORS STARTING")
    left =  GPIO.PWM(C["LEFT_MOTOR_PWM"], 1000)
    right = GPIO.PWM(C["RIGHT_MOTOR_PWM"], 1000)
    left.start(50)
    right.start(50)

def stop_motors(channel):
    '''
    Call back to stop the motors
    '''
    print("MOTORS STOPPING")
    GPIO.PWM(C["LEFT_MOTOR_PWM"], 1000).stop()
    GPIO.PWM(C["RIGHT_MOTOR_PWM"], 1000).stop()

def end(channel):
    ''' 
    To Cleanly terminate the program
    '''
    GPIO.cleanup()
    exit()

def line_found(channel):
    '''
    Called when a line is detected from the sensor
    '''
    print("LINE FOUND")    

if __name__ == "__main__":

  # set up all the pin
  setup()

  # Set up camera module
  camera = PiCamera()
  camera.resolution = (1024, 768)
  camera.start_preview()

  # Set up left motor contorls
  GPIO.output(C["LEFT_MOTOR_SLP"], 1)
  GPIO.output(C["LEFT_MOTOR_DIR"], 0)
  # Set up right motor controls
  GPIO.output(C["RIGHT_MOTOR_SLP"], 1)
  GPIO.output(C["RIGHT_MOTOR_DIR"], 0)

  # Ensure motors begin at stop state
  GPIO.PWM(C["LEFT_MOTOR_PWM"], 1000).stop()
  GPIO.PWM(C["RIGHT_MOTOR_PWM"], 1000).stop()

  print("BUTTON 1 STARTS MOTORS")
  print("BUTTON 2 STOPS MOTORS")
  print("BUTTON 3 ENDS EXECUTION")

  # NOTE: we need to get line sensors working with the event detectors 
  #GPIO.add_event_detect(C["LINE_SENSOR_1"],GPIO.RISING, callback = line_found,bouncetime = 500)
  #GPIO.add_event_detect(C["LINE_SENSOR_4"],GPIO.RISING, callback = line_found,bouncetime = 500)


  # Events for when the buttons are clicked
  # NOTE: All of these are being called correctly however the motors are not being start up
  GPIO.add_event_detect(C["BUTTON1"],GPIO.FALLING, callback = start_motors,bouncetime = 500)
  GPIO.add_event_detect(C["BUTTON2"],GPIO.FALLING, callback = stop_motors,bouncetime = 500)
  GPIO.add_event_detect(C["BUTTON3"],GPIO.FALLING, callback = end,bouncetime = 200)
  GPIO.add_event_detect(C["BUTTON4"],GPIO.FALLING, callback = not_defined,bouncetime = 200)
  GPIO.add_event_detect(C["BUTTON5"],GPIO.FALLING, callback = not_defined,bouncetime = 200)
  GPIO.add_event_detect(C["BUTTON6"],GPIO.FALLING, callback = not_defined,bouncetime = 200)


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