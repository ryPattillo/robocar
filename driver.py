
import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera

from constant import CONSTANTS as C
from pin_setup import setup
from imageReader import detect_signs
from encoder import Encoder
from motor_control import MotorControl

# Configure all the pins
setup()

def print_ticks(ticks):
    '''
    utility function to print the tick data from the encoder
    '''
    print("LEFT WHEEL A CLICKS: ",ticks[0])
    print("LEFT WHEEL B CLICKS: ",ticks[1])
    print()
    print("RIGHT WHEEL A CLICKS: ",ticks[2])
    print("RIGHT WHEEL B CLICKS: ",ticks[3])
    print()

if __name__ == "__main__":

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

    # get necessary objects
    encoder = Encoder()
    motor_control = MotorControl(20)

    # event handlers for when the bumb buttons are clicked
    GPIO.add_event_detect(C["BUTTON1"],GPIO.FALLING, callback = motor_control.drive_forward,bouncetime = 500)
    GPIO.add_event_detect(C["BUTTON2"],GPIO.FALLING, callback = motor_control.stop_motors,bouncetime = 500)
    GPIO.add_event_detect(C["BUTTON3"],GPIO.FALLING, callback = motor_control.end,bouncetime = 200)
    GPIO.add_event_detect(C["BUTTON4"],GPIO.FALLING, callback = motor_control.drive_spin,bouncetime = 200)
    GPIO.add_event_detect(C["BUTTON5"],GPIO.FALLING, callback = motor_control.not_defined,bouncetime = 200)
    GPIO.add_event_detect(C["BUTTON6"],GPIO.FALLING, callback = motor_control.not_defined,bouncetime = 200)

    # event handlers for recieving encoder data
    GPIO.add_event_detect(C["RIGHT_ENCODER_A"],GPIO.BOTH, callback = encoder.read_encoder)
    GPIO.add_event_detect(C["RIGHT_ENCODER_B"],GPIO.BOTH, callback = encoder.read_encoder)
    GPIO.add_event_detect(C["LEFT_ENCODER_A"],GPIO.BOTH, callback = encoder.read_encoder)
    GPIO.add_event_detect(C["LEFT_ENCODER_B"],GPIO.BOTH, callback = encoder.read_encoder)

    # NOTE: sensors are not currently being used
    # GPIO.setup(C["LINE_SENSOR_1"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(C["LINE_SENSOR_2"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(C["LINE_SENSOR_4"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(C["LINE_SENSOR_5"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(C["LINE_SENSOR_7"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(C["LINE_SENSOR_8"], GPIO.IN,pull_up_down = GPIO.PUD_UP)

    TARGET = 500
    SLEEP_TIME = 1
    KP = 0.002

    speed_lm = 20
    speed_rm = 20
    # DUTY CYCLE 50% -> 5 ticks/second

    while True:
        sleep(SLEEP_TIME)

        # get tick data form the encoder class
        ticks = encoder.return_ticks()
        # print_ticks(ticks)
  
        la_error = TARGET - ticks[0]
        lb_error = TARGET - ticks[1]
        ra_error = TARGET - ticks[2]
        rb_error = TARGET - ticks[3]

        speed_lm += (la_error + lb_error) * KP
        speed_rm += (ra_error + rb_error) * KP

        # Ensure we do not set speed faster than 99 or lower than 0
        speed_lm = max(min(99, speed_lm), 0)
        speed_rm = max(min(99, speed_rm), 0)

        # ERROR IS POSITIVE MEAN MOVING TOO FAST
        print("LEFT A ENCODER ERROR: ", la_error)
        print("LEFT B ENCODER ERROR: ", lb_error)
        print("RIGHT A ENCODER ERROR: ", ra_error)
        print("RIGHT B ENCODER ERROR: ", rb_error)
        print("ADJUSTING SPEED TO MINIMIZE ERROR")
        motor_control.change_speed(speed_lm,speed_rm)

        # NOTE: CV not implemented yet
        # img = camera.capture('image.jpg')
        # see if any signs are detected in image
        #if detect_signs():
        #    print("Signs Detected")
        # else:
        #   print("Signs not detected")


        encoder.reset()
