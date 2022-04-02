import RPi.GPIO as GPIO

from constant import CONSTANTS as C
from pin_setup import setup
from imageReader import detect_signs
from encoder import Encoder

class MotorControl:

    started = False

    def __init__(self,speed):
        # set up left and right motor controls
        # NOTE:  motors should initally be off, [SLP = 1]
        GPIO.output(C["RIGHT_MOTOR_SLP"], 1)
        GPIO.output(C["LEFT_MOTOR_SLP"], 1)
        # set right and left motor equal to the PWM pins
        # NOTE: 2nd refers to the frequencyof the PWM
        self.right_motor = GPIO.PWM(C["RIGHT_MOTOR_PWM"], 1000)
        self.left_motor =  GPIO.PWM(C["LEFT_MOTOR_PWM"], 1000)
        # motors initially should be stopped
        self.right_motor.stop()
        self.left_motor.stop()
        self.speed = speed

    def drive_forward(self,channel):
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
        self.left_motor.start(self.speed)
        self.right_motor.start(self.speed)

        self.started = True
        

    def stop_motors(self,channel):
        '''
        callback to stop the motors
        '''
        print("MOTORS STOPPING...........")
        self.left_motor.stop()
        self.right_motor.stop()
        self.started = False


    def drive_spin(self,channel):
        '''
        callback for driving robot in spin mode
        '''
        # left motor will go in reverse and right will go forward
        GPIO.output(C["LEFT_MOTOR_DIR"], 1)
        GPIO.output(C["RIGHT_MOTOR_DIR"], 0)

        # start motors with duty cycle 50%
        self.left_motor.start(self.speed)
        self.right_motor.start(self.speed)

        self.started = True


    def not_defined(self,channel):
        '''
        callback that currently
        '''
        print("BUTTON IS NOT BEING USED")

    def end(self,channel):
        ''' 
        cleanly exit the program and clear defined pins
        '''
        GPIO.cleanup()
        exit()

    def change_speed(self,speed_lm,speed_rm):
        '''
        change the speed of the motors
        '''

        if self.started:
            print("LEFT MOTOR SPEED BEING ADJUSTED TO ",speed_lm,"%")
            print("RIGHT MOTOR SPEED BEING ADJUSTED TO ",speed_rm,"%")
            self.left_motor.ChangeDutyCycle(speed_lm)
            self.right_motor.ChangeDutyCycle(speed_rm)
        else:
            print("MOTORS HAVE NOT BEEN STARTED")    