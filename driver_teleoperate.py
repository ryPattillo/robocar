import RPi.GPIO as GPIO
from time import sleep
from constant import CONSTANTS as C
from pin_setup import setup
from picamera import PiCamera
from pynput import keyboard

# setup()
# left =  GPIO.PWM(C["LEFT_MOTOR_PWM"], 1000)
# right = GPIO.PWM(C["RIGHT_MOTOR_PWM"], 1000)

def on_press(key):
  try:
	#if(key == keyboard.Key.right):
		#print("clicked right arrow key")
    
	print('Alphanumeric key pressed: {0} '.format(key.char))
  except AttributeError:
    print('special key pressed: {0}'.format(key))

def on_release(key):
  print('Key released: {0}'.format(key))
  if key == keyboard.Key.esc:
	# Exit Program
	exit()
    # Stop listener
    #return False

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



    #sleep(0.5)
    left.start(50)
    right.start(50)

def stop_motors(channel):
    '''
    Call back to stop the motors
    '''
    print("MOTORS STOPPING")
    left.stop()
    right.stop()

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


  # Set up camera module
  #camera = PiCamera()
  #camera.resolution = (1024, 768)
  #camera.start_preview()
  
  print('Press any Key')

  # Collect events until released
  with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

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
