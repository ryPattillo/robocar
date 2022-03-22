import RPi.GPIO as GPIO
from constant import CONSTANTS as C

def setup():
    # Set mode
    GPIO.setmode(GPIO.BCM)

    # Configure Bumb Sensors
    GPIO.setup(C["BUTTON1"], GPIO.IN)
    GPIO.setup(C["BUTTON2"], GPIO.IN)
    # NOTE: Pull up resistors: put the power between +V and signal
    # NOTE: Pull down resistors: Put in between +v and ground (-v)  
    GPIO.setup(C["BUTTON3"], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(C["BUTTON4"], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(C["BUTTON5"], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(C["BUTTON6"], GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # Configure left motor
    GPIO.setup(C["LEFT_MOTOR_SLP"], GPIO.OUT)
    GPIO.setup(C["LEFT_MOTOR_DIR"], GPIO.OUT)
    GPIO.setup(C["LEFT_MOTOR_PWM"], GPIO.OUT)

    # Configure right motor
    GPIO.setup(C["RIGHT_MOTOR_SLP"], GPIO.OUT)
    GPIO.setup(C["RIGHT_MOTOR_DIR"], GPIO.OUT)
    GPIO.setup(C["RIGHT_MOTOR_PWM"], GPIO.OUT)

    # The led needed for the light sensors to work
    GPIO.setup(C["LINE_SENSOR_LED"], GPIO.OUT)

    # Allow for input from each of the sensors
    GPIO.setup(C["LINE_SENSOR_1"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.setup(C["LINE_SENSOR_2"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.setup(C["LINE_SENSOR_4"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.setup(C["LINE_SENSOR_5"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.setup(C["LINE_SENSOR_7"], GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.setup(C["LINE_SENSOR_8"], GPIO.IN,pull_up_down = GPIO.PUD_UP)

