
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

def pid(target,kp,ticks,lm_speed,rm_speed):
    '''
    calculate new speed based on encoder data, target, and kp
    '''
    # compute error
    la_error = target - ticks[0]
    lb_error = target - ticks[1]
    ra_error = target - ticks[2]
    rb_error = target - ticks[3]

    # adjust spped accordingly
    lm_speed += (la_error + lb_error) * kp
    rm_speed += (ra_error + rb_error) * kp

    # ensure we do not set speed faster than 99 or lower than 0
    lm_speed = max(min(99, lm_speed), 0)
    rm_speed = max(min(99, rm_speed), 0)

    return lm_speed,rm_speed

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

def print_error(la_error,lb_error,ra_error,rb_error):
    '''
    utility function to print out encoder error
    '''
    print("LEFT A ENCODER ERROR: ", la_error)
    print("LEFT B ENCODER ERROR: ", lb_error)
    print("RIGHT A ENCODER ERROR: ", ra_error)
    print("RIGHT B ENCODER ERROR: ", rb_error)
    print("ADJUSTING SPEED TO MINIMIZE ERROR")

def calibrate_encoders(motor_control,encoder,seconds):
    '''
    utility function to calibrate encoder speed
    this used to see how the change in duty cycle will affect the encoder readings
    this information will help me get encoder duty cycle info from encoders
    '''
    ticks = (0,0,0,0)
    if motor_control.started:
        # try each speed
        for speed in range(20,99):
            # reset encoders
            encoder.reset()
            # bump up speed
            motor_control.change_speed(speed,speed)
            # sleep for certain amount of time
            sleep(seconds)
            # hold on to previous tick numbers
            prev_left_ticks = ticks[0] + ticks[1]
            prev_right_ticks = ticks[1] + ticks[2]
            # see how ticks are changing
            ticks = encoder.return_ticks()
            left_ticks = ticks[0] + ticks[1]
            right_ticks = ticks[2] + ticks[3]

            print("LEFT ENCODER TICKS  [%d] | CHANGE FROM PREVIOUS [%d]" % (left_ticks, left_ticks - prev_left_ticks))
            print("RIGHT ENCODER TICKS [%d] | CHANGE FROM PREVIOUS [%d]" % (right_ticks,right_ticks - prev_right_ticks))
            print("RATIO OF LEFT TICKS TO SPEED %f" % (left_ticks / speed))
            print("RATIO OF RIGHT TICKS TO SPEED %f"% (right_ticks / speed))
            print()
    else:
        print("Motor must be started first")

if __name__ == "__main__":

    # NOTE: following code is for camera module that is not implemented yet
    # Set up camera module
    # camera = PiCamera()
    # TODO: Figure out what resolution works well
    # camera.resolution = (1024, 768)
    # camera.start_preview()

    # user instructions
    print("BUTTON 1 START MOTORS")
    print("BUTTON 2 STOPS MOTORS")
    print("BUTTON 3 ENDS EXECUTION")
    print("BUTTON 4 DRIVES ROBOT IN SPIN MODE")

    # get necessary objects
    encoder = Encoder()
    motor_control = MotorControl(20)

    # event handlers for when the bumb buttons are clicked
    GPIO.add_event_detect(C["BUTTON1"],GPIO.FALLING, callback = motor_control.start,bouncetime = 500)
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

    SLEEP_TIME = 1
    target_ticks = 2770
    kp = 0.00002
    lm_speed = 50
    rm_speed = 50

    timer = 0
    while True:
        sleep(SLEEP_TIME)
        # get tick data form the encoder class
        ticks = encoder.return_ticks()
        
        # NOTE: following function call are just utility
        # print_ticks(ticks)
        # calibrate_encoders(motor_control,encoder,1)

        # get the left and right speed adjustments
        lm_speed,rm_speed = pid(target_ticks,kp,ticks,lm_speed,rm_speed)
        motor_control.change_speed(lm_speed,rm_speed)
        encoder.reset()
        # timer used just for testing
        timer += 1
        if timer % 5 == 0:
            # turn robot right after 10 seconds
            motor_control.turn_right()
        # elif timer % 5 == 0:
        #     # turn robot left after 10 seconds
        #     motor_control.turn_left()

        # NOTE: CV not implemented yet
        # img = camera.capture('image.jpg')
        # see if any signs are detected in image
        #if detect_signs():
        #    print("Signs Detected")
        # else:
        #   print("Signs not detected")
