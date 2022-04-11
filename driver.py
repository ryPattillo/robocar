""" Module for driving the robot. 
Interacts with al the motor controls and 
encoder information
"""
import RPi.GPIO as GPIO
from time import sleep

from constant import CONSTANTS as C
from pin_setup import setup
from encoder import Encoder
from motor_control import MotorControl
import keyboard

# NOTE: uncomment if time for CV
# from imageReader import detect_signs

class Driver: 
 
    def __init__(self,drive_mode,cruising_speed):
        self.motor_control = MotorControl()
        self.lm_speed = 0
        self.rm_speed = 0
        self.cruising_speed = cruising_speed
        self.drive_mode = drive_mode
        self.encoder = Encoder()
 
    def pid(self,target,kp,ticks):
        """ Calculate new speed based on encoder data, target, and kp. 
        Used for stabilization on freeroam
        """

        # The ticks that the encoders should be reading
        target_ticks = 2770
        # How much to update the speed based on error
        kp = 0.00002

        lm_speed = self.motor_control.lm_speed
        rm_speed = self.motor_control.rm_speed

        la_error = target_ticks - ticks[0]
        lb_error = target_ticks - ticks[1]
        ra_error = target_ticks - ticks[2]
        rb_error = target_ticks - ticks[3]

        self.lm_speed += (la_error + lb_error) * kp
        self.rm_speed += (ra_error + rb_error) * kp

        # Ensure we do not set speed faster than 99 or lower than 0
        self.lm_speed = max(min(99, self.lm_speed), 0)
        self.rm_speed = max(min(99, self.key_pressrm_speed), 0)

        self.motor_control.change_speed(lm_speed,rm_speed)

    def print_ticks(self,ticks):
        """ Utility print function to print the tick data from the encoder
        """

        print("LEFT WHEEL A CLICKS: ",ticks[0])
        print("LEFT WHEEL B CLICKS: ",ticks[1])
        print()
        print("RIGHT WHEEL A CLICKS: ",ticks[2])
        print("RIGHT WHEEL B CLICKS: ",ticks[3])
        print()

    def print_error(self,la_error,lb_error,ra_error,rb_error):
        """ Utility print function to print out encoder error
        """

        print("LEFT A ENCODER ERROR: ", la_error)
        print("LEFT B ENCODER ERROR: ", lb_error)
        print("RIGHT A ENCODER ERROR: ", ra_error)
        print("RIGHT B ENCODER ERROR: ", rb_error)
        print("ADJUSTING SPEED TO MINIMIZE ERROR")

    def calibrate_encoders(self,encoder,seconds):
        """ Utility function to calibrate encoder speed
        this used to vsee how the change in duty cycle will affect the encoder readings
        this information will help me get encoder duty cycle info from encoders
        '"""
        
        ticks = (0,0,0,0)

        if self.motor_control.started:
            # try each speed
            for speed in range(20,99):
                # reset encoders
                encoder.reset()
                # bump up speed
                self.motor_control.change_speed(speed,speed)
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
            print("MOTORS MUST BE STARTED FIRST")


    def key_press(self,key):
        """ keyboard listener for teleop
        """

        # start the motor
        if key.name == "enter":
            self.lm_speed = self.cruising_speed
            self.rm_speed = self.cruising_speed
            self.motor_control.start(0,0)
        # kill the program
        elif key.name == "delete":
            self.motor_control.end(0)
        # turn the motor left
        # NOTE: when increasing right motor speed, left must be restored to default
        elif key.name == "left":
            self.lm_speed = self.cruising_speed
            self.rm_speed += 1
        # NOTE: when increasing right motor speed, right must be restored to cruise
        elif key.name == "right":
            self.lm_speed += 1
            self.rm_speed = self.cruising_speed
        # increase the crusing speed
        elif key.name == "up":
            self.cruising_speed += 1
            self.lm_speed = self.cruising_speed
            self.rm_speed = self.cruising_speed
        # decrease the cruising speed
        elif key.name == "down":
            self.cruising_speed -= 1
            self.lm_speed = self.cruising_speed
            self.rm_speed = self.cruising_speed
        # emergency break
        elif key.name == "shift":
            self.cruising_speed = 10
            self.lm_speed = 10
            self.rm_speed = 10   
        # reverse
        elif key.name == "return":
            self.motor_control.change_direction(0)
        # nitrous    
        elif key.name == "space":
            self.cruising_speed += 15
            self.lm_speed = self.cruising_speed
            self.rm_speed = self.cruising_speed
        # change to updated speed    
        self.motor_control.change_speed(self.lm_speed,self.rm_speed)

    def add_interrupts(self):
        """ All the button sensors and encoder interrupts
        """

        # robot should reverse when it hits something
        GPIO.add_event_detect(C["BUTTON1"],GPIO.FALLING, callback = self.motor_control.end,bouncetime = 500)
        GPIO.add_event_detect(C["BUTTON2"],GPIO.FALLING, callback = self.motor_control.change_direction,bouncetime = 500)
        GPIO.add_event_detect(C["BUTTON3"],GPIO.FALLING, callback = self.motor_control.change_direction,bouncetime = 200)
        GPIO.add_event_detect(C["BUTTON4"],GPIO.FALLING, callback = self.motor_control.change_direction,bouncetime = 200)
        GPIO.add_event_detect(C["BUTTON5"],GPIO.FALLING, callback = self.motor_control.change_direction,bouncetime = 200)
        GPIO.add_event_detect(C["BUTTON6"],GPIO.FALLING, callback = self.motor_control.change_direction,bouncetime = 200)
        # event handlers for recieving encoder data
        GPIO.add_event_detect(C["RIGHT_ENCODER_A"],GPIO.BOTH, callback = self.encoder.read_encoder)
        GPIO.add_event_detect(C["RIGHT_ENCODER_B"],GPIO.BOTH, callback = self.encoder.read_encoder)
        GPIO.add_event_detect(C["LEFT_ENCODER_A"],GPIO.BOTH, callback =  self.encoder.read_encoder)
        GPIO.add_event_detect(C["LEFT_ENCODER_B"],GPIO.BOTH, callback =  self.encoder.read_encoder)

    def drive(self):
        # Ensure interrupts are setup
        self.add_interrupts()

        if self.drive_mode == 0:
            # start the motor at a default cruising spped
            self.motor_control.start(self.cruising_speed,self.cruising_speed)
        elif self.drive_mode == 1:
            # keyboard listener
            keyboard.on_press(self.key_press)
        elif self.drive_mode == 2:
            # instructed mode
            pass
        # sleep for a certain amount of time in while loop                  
        SLEEP_TIME = 1
        while True:
            sleep(SLEEP_TIME)
            # free drive mode
            if self.drive_mode == 0:
                # free-roam should utlize stablization
                ticks = self.encoder.return_ticks()
                self.pid(ticks)
            # teleop mode
            elif self.drive_mode == 1: 
                pass
            # path planning
            elif self.drive_mode == 2:
                pass
            # calibration mode
            elif self.drive_mode == 3:
                self.calibrate_encoders()

            self.encoder.reset()

    

    
    


