
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
    la_error = target - ticks[0]
    lb_error = target - ticks[1]
    ra_error = target - ticks[2]
    rb_error = target - ticks[3]

    lm_speed += (la_error + lb_error) * KP
    rm_speed += (ra_error + rb_error) * KP

    # Ensure we do not set speed faster than 99 or lower than 0
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
    Utility function to print out encoder error
    '''
    print("LEFT A ENCODER ERROR: ", la_error)
    print("LEFT B ENCODER ERROR: ", lb_error)
    print("RIGHT A ENCODER ERROR: ", ra_error)
    print("RIGHT B ENCODER ERROR: ", rb_error)
    print("ADJUSTING SPEED TO MINIMIZE ERROR")

def calibrate_encoders(motor_control,encoder,seconds):
    '''
    utility function to calibrate encoder speed
    this used to vsee how the change in duty cycle will affect the encoder readings
    this information will help me get encoder duty cycle info from encoders
    '''

    if motor_control.started:
        # try each speed
        for speed in range(99):
            # reset encoders
            encoder.reset()
            # bump up speed
            motor_control.change_speed(speed,speed)
            # sleep for certain amount of time
            sleep(seconds)
            # hold on to previous tick numbers
            prev_ticks = ticks
            # see how ticks are changing
            ticks = encoder.return_ticks()

            print("DUTY CYCLE [%d]")
            print("LEFT ENCODER A TICKS  [%d] | CHANGE FROM PREVIOUS [%d]" % (ticks[0],ticks[0] - prev_ticks[0]) )
            print("LEFT ENCODER B TICKS  [%d] | CHANGE FROM PREVIOUS [%d]" % (ticks[1],ticks[1] - prev_ticks[1]))
            print("RIGHT ENCODER A TICKS [%d] | CHANGE FROM PREVIOUS [%d]" % (ticks[2],ticks[2] - prev_ticks[2]))
            print("RIGHT ENCODER B TICKS [%d] | CHANGE FROM PREVIOUS [%d]" % (ticks[3],ticks[3] - prev_ticks[3]))
            print()
    else:
        print("Motor must be started first")

if __name__ == "__main__":

    # NOTE: following code is for camera module that is not implemented yet
    # Set up camera module
    # camera = PiCamera()
    # TODO: Figure out what resolution works well
    #camera.resolution = (1024, 768)
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

    SLEEP_TIME = 2



    target = 100
    kp = 0.002
    lm_speed = 0
    rm_speed = 0

    while True:
        sleep(SLEEP_TIME)
        # get tick data form the encoder class
        ticks = encoder.return_ticks()
        # print_ticks(ticks)
        
        # calbirate the encoder
        calibrate_encoders(motor_control,encoder,1)
        #lm_speed,rm_spped = pid(target,kp,ticks,lm_speed,rm_speed)
        #motor_control.change_speed(lm_speed,rm_speed)

        # NOTE: CV not implemented yet
        # img = camera.capture('image.jpg')
        # see if any signs are detected in image
        #if detect_signs():
        #    print("Signs Detected")
        # else:
        #   print("Signs not detected")


        encoder.reset()
