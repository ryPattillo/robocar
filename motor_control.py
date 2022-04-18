""" Motor control module. All the functionality for for driving the robot
"""

import RPi.GPIO as GPIO

from constant import CONSTANTS as C
from pin_setup import setup
from encoder import Encoder
from time import sleep

class MotorControl:
    # keep track of if motors have been started
    started = False

    def __init__(self):
        # set up left and right motor controls
        # NOTE:  motors should initally be off, [SLP = 1]
        GPIO.output(C["RIGHT_MOTOR_SLP"], 0)
        GPIO.output(C["LEFT_MOTOR_SLP"], 0)
        # set right and left motor equal to the PWM pins
        # NOTE: 2nd refers to the frequency of the PWM
        self.right_motor = GPIO.PWM(C["RIGHT_MOTOR_PWM"], 1000)
        self.left_motor =  GPIO.PWM(C["LEFT_MOTOR_PWM"], 1000)
        # motors initially should be stopped
        self.right_motor.stop()
        self.left_motor.stop()
        # should initially be going forward
        self.lm_dir = 0    
        self.rm_dir = 0      


    def start(self,start_lm,start_rm):
        """ Start the motors given starting speeds for the left 
        and right motors
        """
        # NOTE: The motors are not being start up for some reason
        print("LEFT MOTOR SPEED BEING ADJUSTED TO ",start_lm,"%")
        print("RIGHT MOTOR SPEED BEING ADJUSTED TO ",start_rm,"%")
        # Assign direction
        GPIO.output(C["LEFT_MOTOR_DIR"], self.lm_dir)
        GPIO.output(C["RIGHT_MOTOR_DIR"], self.rm_dir)
        # Should be initially stopped
        GPIO.output(C["RIGHT_MOTOR_SLP"], 1)
        GPIO.output(C["LEFT_MOTOR_SLP"], 1)
        # motors started with a duty cycle of 50%
        self.left_motor.start(start_lm)
        self.right_motor.start(start_rm)
        # mark that motors have started
        self.started = True    

    def stop_motors(self):
        """ Stop the motors
        """ 
        if self.started:
            print("MOTORS STOPPING...........")
            self.left_motor.stop()
            self.right_motor.stop()
            self.started = False
        else:
            print("MOTORS ARE ALREADY STOPPED")


    def reverse(self):
        if self.lm_dir and self.rm_dir:
            self.change_direction(True,True)
        else:
            print("ALREADY GOING BACKWARDS")
            return False
        return True
        

    def turn_around(self,channel):
        """ Turn the robot around
        """

        # start going backward
        self.change_direction(True,True)
        # increase spped to turn
        self.change_speed(40,20)
        sleep(1)
        # restore speed back
        self.change_speed(30,30)
        self.change_direction(True,True)

    def change_direction(self,lm,rm):
        """ Change the current direction of the robot
        """
        if lm and rm:
            self.lm_dir = not self.lm_dir
            self.rm_dir = not self.rm_dir
        elif lm:
            self.lm_dir = not self.lm_dir
        elif rm:
            self.rm_dir = not self.rm_dir

        # Switch directions
        GPIO.output(C["LEFT_MOTOR_DIR"], self.lm_dir)
        GPIO.output(C["RIGHT_MOTOR_DIR"], self.rm_dir)


    def end(self,channel):
        """ Cleanly exit the program and clear pins 
        that have been defined
        """    
        # Stop the motors
        self.left_motor.stop()
        self.right_motor.stop()
        GPIO.cleanup()
        exit()

    def change_speed(self,speed_lm,speed_rm):
        """ Change the speed of the motors
        """
        print("-----------------------------------")
        if self.started:
            if speed_lm >99 or speed_rm > 99:
                print("MOTORS AT MAX SPEED")
                return
            elif speed_lm < 0 or speed_rm < 0:
                print("MOTORS AT MIN SPEED")
                return     
            else:
                print("LEFT MOTOR SPEED BEING ADJUSTED TO ",speed_lm,"%")
                print("RIGHT MOTOR SPEED BEING ADJUSTED TO ",speed_rm,"%")
                self.left_motor.ChangeDutyCycle(speed_lm)
                self.right_motor.ChangeDutyCycle(speed_rm)
        else:
            print("MOTORS HAVE NOT BEEN STARTED")    
        print("-----------------------------------")
