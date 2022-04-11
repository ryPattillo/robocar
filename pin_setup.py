import RPi.GPIO as GPIO
from constant import CONSTANTS as C

def setup():
    '''
    Function just for setting up all the pins, more organized then having this 
    all in the driver file
    '''
    GPIO.setwarnings(False)
    # Set mode
    GPIO.setmode(GPIO.BCM)

    # Bumb Sensors
    # NOTE: Pull up resistors: put the power between +V and signal
    # NOTE: Pull down resistors: Put in between +v and ground (-v) 
    GPIO.setup(C["BUTTON1"], GPIO.IN)
    GPIO.setup(C["BUTTON2"], GPIO.IN) 
    GPIO.setup(C["BUTTON3"], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(C["BUTTON4"], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(C["BUTTON5"], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(C["BUTTON6"], GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # Configure left motor pins
    GPIO.setup(C["LEFT_MOTOR_SLP"], GPIO.OUT)
    GPIO.setup(C["LEFT_MOTOR_DIR"], GPIO.OUT)
    GPIO.setup(C["LEFT_MOTOR_PWM"], GPIO.OUT)

    # Configure right motor pins
    GPIO.setup(C["RIGHT_MOTOR_SLP"], GPIO.OUT)
    GPIO.setup(C["RIGHT_MOTOR_DIR"], GPIO.OUT)
    GPIO.setup(C["RIGHT_MOTOR_PWM"], GPIO.OUT)

    # Configure encoder pins
    GPIO.setup(C["LEFT_ENCODER_A"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.setup(C["LEFT_ENCODER_B"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.setup(C["RIGHT_ENCODER_A"],GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.setup(C["RIGHT_ENCODER_B"],GPIO.IN,pull_up_down = GPIO.PUD_UP)