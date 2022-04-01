
import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera

from constant import CONSTANTS as C
from pin_setup import setup
from imageReader import detect_signs

# Configure all the pins
setup()

# set up left and right motor controls
# NOTE:  motors should initally be off, [SLP = 1]
GPIO.output(C["RIGHT_MOTOR_SLP"], 1)
GPIO.output(C["LEFT_MOTOR_SLP"], 1)
# set right and left motor equal to the PWM pins
# NOTE: 2nd refers to the frequencyof the PWM
right_motor = GPIO.PWM(C["RIGHT_MOTOR_PWM"], 1000)
left_motor =  GPIO.PWM(C["LEFT_MOTOR_PWM"], 1000)
# motors initially should be stopped
left_motor.stop()
right_motor.stop()


def drive_forward(channel):
    '''
    call back for starting the motors forward
    '''
    # NOTE: The motors are not being start up for some reason
    print("FORWARD DRIVE STARTING........")

    # direction should be forward[0]
    GPIO.output(C["LEFT_MOTOR_DIR"], 0)
    GPIO.output(C["RIGHT_MOTOR_DIR"], 0)
    
    # sleep should be disabled 
    GPIO.output(C["RIGHT_MOTOR_SLP"], 1)
    GPIO.output(C["LEFT_MOTOR_SLP"], 1)

    # motors started with a duty cycle of 50%
    left_motor.start(50)
    right_motor.start(50)
    

def stop_motors(channel):
    '''
    callback to stop the motors
    '''
    print("MOTORS STOPPING...........")
    left_motor.stop()
    right_motor.stop()

def drive_spin(channel):
    '''
    callback for driving robot in spin mode
    '''
    # left motor will go in reverse and right will go forward
    GPIO.output(C["LEFT_MOTOR_DIR"], 1)
    GPIO.output(C["RIGHT_MOTOR_DIR"], 0)

    # start motors with duty cycle 50%
    left_motor.start(50)
    right_motor.start(50)

def read_encoder(channel):
    '''
    callback for reading encoder data
    '''
    global total_clicks_la
    global total_clicks_lb 
    global total_clicks_ra
    global total_clicks_rb 

    if channel == 23:
        total_clicks_lb += 1
    if channel == 24:
        total_clicks_la += 1
    if channel == 25:
        total_clicks_ra += 1
    if channel == 26:
        total_clicks_rb += 1


def not_defined(channel):
    '''
    callback that currently
    '''
    print("BUTTON IS NOT BEING USED")


def end(channel):
    ''' 
    cleanly exit the program and clear defined pins
    '''
    GPIO.cleanup()
    exit()


if __name__ == "__main__":

    global total_clicks_la
    global total_clicks_lb 
    global total_clicks_ra
    global total_clicks_rb

    total_clicks_la = 0
    total_clicks_lb = 0
    total_clicks_ra = 0
    total_clicks_rb = 0
 
    # NOTE: following code is for camera module that is not implemented yet
    # Set up camera module
    # camera = PiCamera()
    # TODO: Figure out what resolution works well
    #camera.resolution = (1024, 768)
    # camera.start_preview()

    # user instructions
    print("BUTTON 1 MOVE ROBOT FORWARD")
    print("BUTTON 2 STOPS MOTORS")
    print("BUTTON 3 ENDS EXECUTION")
    print("BUTTON 4 DRIVES ROBOT IN SPIN MODE")

    # event handlers for when the bumb buttons are clicked
    GPIO.add_event_detect(C["BUTTON1"],GPIO.FALLING, callback = drive_forward,bouncetime = 500)
    GPIO.add_event_detect(C["BUTTON2"],GPIO.FALLING, callback = stop_motors,bouncetime = 500)
    GPIO.add_event_detect(C["BUTTON3"],GPIO.FALLING, callback = end,bouncetime = 200)
    GPIO.add_event_detect(C["BUTTON4"],GPIO.FALLING, callback = drive_spin,bouncetime = 200)
    GPIO.add_event_detect(C["BUTTON5"],GPIO.FALLING, callback = not_defined,bouncetime = 200)
    GPIO.add_event_detect(C["BUTTON6"],GPIO.FALLING, callback = not_defined,bouncetime = 200)

    # event handlers for recieving encoder data
    GPIO.add_event_detect(C["RIGHT_ENCODER_A"],GPIO.BOTH, callback = read_encoder,bouncetime = 200)
    GPIO.add_event_detect(C["RIGHT_ENCODER_B"],GPIO.BOTH, callback = read_encoder,bouncetime = 200)
    GPIO.add_event_detect(C["LEFT_ENCODER_A"],GPIO.BOTH, callback = read_encoder,bouncetime = 200)
    GPIO.add_event_detect(C["LEFT_ENCODER_B"],GPIO.BOTH, callback = read_encoder,bouncetime = 200)

    # NOTE: sensors are not currently being used
    # GPIO.setup(C["LINE_SENSOR_1"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(C["LINE_SENSOR_2"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(C["LINE_SENSOR_4"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(C["LINE_SENSOR_5"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(C["LINE_SENSOR_7"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(C["LINE_SENSOR_8"], GPIO.IN,pull_up_down = GPIO.PUD_UP)

    while True:

        sleep(2)
        print("LEFT WHEEL A CLICKS: ",total_clicks_la)
        print("LEFT WHEEL B CLICKS: ",total_clicks_lb)
        print()
        print("RIGHT WHEEL A CLICKS: ",total_clicks_ra)
        print("RIGHT WHEEL B CLICKS: ",total_clicks_rb)
        print()

        # NOTE: CV not implemented yet
        # img = camera.capture('image.jpg')
        # see if any signs are detected in image
        #if detect_signs():
        #    print("Signs Detected")
        # else:
        #   print("Signs not detected")



