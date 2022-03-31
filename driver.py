
import RPi.GPIO as GPIO
from time import sleep
from constant import CONSTANTS as C
from pin_setup import setup
from picamera import PiCamera
from imageReader import detect_signs

# Configure all the pins
setup()

# Set up left motor controls
GPIO.output(C["LEFT_MOTOR_SLP"], 1)
GPIO.output(C["LEFT_MOTOR_DIR"], 0)

# Set up right motor controls
GPIO.output(C["RIGHT_MOTOR_SLP"], 1)
GPIO.output(C["RIGHT_MOTOR_DIR"], 0)

left =  GPIO.PWM(C["LEFT_MOTOR_PWM"], 1000)
right = GPIO.PWM(C["RIGHT_MOTOR_PWM"], 1000)

#### ALL THE MOTOR CONTROL FUNCTIONS ###

def start_motors(channel):
    '''
    Call back to start the motors
    '''

    # NOTE: The motors are not being start up for some reason
    print("MOTORS STARTING")

    left.start(50)
    right.start(50)

def stop_motors(channel):
    '''
    Call back to stop the motors
    '''
    print("MOTORS STOPPING")
    left.stop()
    right.stop()

def turn_left():
    '''
    Function turn robot to the left
    '''
    pass

def turn_right():
    '''
    Function to turn robot to the right
    '''
    pass

def speed_up():
    '''
    Function to speed up robot
    '''
    pass

def slow_down():  
    '''
    Function to slow down robot
    '''
    pass

#############################################


############ UTILITY CALLBACKS ###############

def not_defined(channel):
    '''
    Callback that does nothing
    '''
    print("BUTTON HAS NO FUNCTIOALITY")


def end(channel):
    ''' 
    To Cleanly terminate the program
    '''
    GPIO.cleanup()
    exit()

#################################################

if __name__ == "__main__":

    # Set up camera module
    camera = PiCamera()

    # TODO: Figure out what resolution works well
    camera.resolution = (1024, 768)
    camera.start_preview()

    # We want the motors to be initially stoped
    left.stop()
    right.stop()

    # USER GUIDE
    print("BUTTON 1 STARTS MOTORS")
    print("BUTTON 2 STOPS MOTORS")
    print("BUTTON 3 ENDS EXECUTION")

    # Events for when the buttons are clicked
    GPIO.add_event_detect(C["BUTTON1"],GPIO.FALLING, callback = start_motors,bouncetime = 500)
    GPIO.add_event_detect(C["BUTTON2"],GPIO.FALLING, callback = stop_motors,bouncetime = 500)
    GPIO.add_event_detect(C["BUTTON3"],GPIO.FALLING, callback = end,bouncetime = 200)
    GPIO.add_event_detect(C["BUTTON4"],GPIO.FALLING, callback = not_defined,bouncetime = 200)
    GPIO.add_event_detect(C["BUTTON5"],GPIO.FALLING, callback = not_defined,bouncetime = 200)
    GPIO.add_event_detect(C["BUTTON6"],GPIO.FALLING, callback = not_defined,bouncetime = 200)

    # TODO: Allow for input from each of the sensors
    # GPIO.setup(C["LINE_SENSOR_1"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(C["LINE_SENSOR_2"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(C["LINE_SENSOR_4"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(C["LINE_SENSOR_5"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(C["LINE_SENSOR_7"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(C["LINE_SENSOR_8"], GPIO.IN,pull_up_down = GPIO.PUD_UP)

    while True:
        pass
     
        # TODO: work on CV after motor control worked out
        # Capture an image every 2 seconds
        # sleep(2)
        # img = camera.capture('image.jpg')

        # see if any signs are detected in image
        #if detect_signs():
        #    print("Signs Detected")
        # else:
        #   print("Signs not detected")