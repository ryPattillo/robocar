import RPi.GPIO as GPIO

from constant import CONSTANTS as C
from pin_setup import setup
#from imageReader import detect_signs
from encoder import Encoder

from time import sleep

class MotorControl:
    # keep track of if motors have been started
    started = False

    def __init__(self):
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
        # should initially be going forward
        self.dir = 0      

    def start(self,start_lm,start_rm):
        '''
        call back for starting the motors
        start will set the direction and turn off sleep but not change speed
        '''
        # NOTE: The motors are not being start up for some reason
        print("MOTORS STARTING UP........")
        # sleep should be disabled 
        GPIO.output(C["LEFT_MOTOR_DIR"], self.dir)
        GPIO.output(C["RIGHT_MOTOR_DIR"], self.dir)

        GPIO.output(C["RIGHT_MOTOR_SLP"], 1)
        GPIO.output(C["LEFT_MOTOR_SLP"], 1)
        # motors started with a duty cycle of 50%
        self.left_motor.start(start_lm)
        self.right_motor.start(start_rm)
        # mark that motors have started
        self.started = True    

    def stop_motors(self,channel):
        '''
        callback to stop the motors
        '''
        print("MOTORS STOPPING...........")
        self.left_motor.stop()
        self.right_motor.stop()
        self.started = False

    def change_direction(self,channel):
        '''
        change the current direction of the robot
        '''
        self.dir = not self.dir
        GPIO.output(C["LEFT_MOTOR_DIR"], self.dir)
        GPIO.output(C["RIGHT_MOTOR_DIR"], self.dir)

    def not_defined(self,channel):
        '''
        callback that currently
        '''
        print("BUTTON IS NOT BEING USED")

    def end(self,channel):
        ''' 
        cleanly exit the program and clear defined pins
        '''        
        # stop the motors
        self.left_motor.stop()
        self.right_motor.stop()
        GPIO.cleanup()
        exit()

    def change_speed(self,speed_lm,speed_rm):
        '''
        change the speed of the motors
        '''

        if speed_lm >= 99 or speed_rm >= 99:
            print("motors cannot go any faster")
            return
        if speed_lm <= 0 or speed_rm <- 0:
            print("motors cannot go any slower")
            return     

        if self.started:
            print("LEFT MOTOR SPEED BEING ADJUSTED TO ",speed_lm,"%")
            print("RIGHT MOTOR SPEED BEING ADJUSTED TO ",speed_rm,"%")
            self.left_motor.ChangeDutyCycle(speed_lm)
            self.right_motor.ChangeDutyCycle(speed_rm)
        else:
            print("MOTORS HAVE NOT BEEN STARTED")    
