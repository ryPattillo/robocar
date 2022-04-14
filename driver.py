""" Main module for driving the robot
"""
import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera
import keyboard

from constant import CONSTANTS as C
from encoder import Encoder
from motor_control import MotorControl
from vision import detect_signs, detect_faces

class Driver: 
 
    def __init__(self,drive_mode,cruising_speed):
        self.motor_control = MotorControl()
        # Speed should be 0 for both motors initially
        self.lm_speed = 0
        self.rm_speed = 0
        # Speed that motors should be restored to after turning
        self.cruising_speed = cruising_speed
        self.drive_mode = drive_mode
        self.encoder = Encoder()
        # Set up camera
        self.camera = PiCamera()
        self.camera.resolution = (1080,768)


    def key_press(self,key):
        """ keyboard listener for teleop
        """

        # start the motor
        if key.name == "enter":
            self.update_speed(self.cruising_speed,self.cruising_speed)
            self.motor_control.start(0,0)
        # NOTE: when increasing right motor speed, left must be restored to default
        elif key.name == "a":
            self.update_speed(self.cruising_speed,self.rm_speed + 1)
        # NOTE: when increasing right motor speed, right must be restored to cruise
        elif key.name == "d":
            self.update_speed(self.lm_speed + 1,self.cruising_speed)
        # forward drive
        elif key.name == "w":
            if self.cruising_speed <= 0 and self.motor_control.dir:
                self.motor_control.change_direction(True,True)
            elif self.motor_control.dir:
                self.cruising_speed -= 3
                self.update_speed(self.cruising_speed,self.cruising_speed)
            else:
                self.cruising_speed += 3
                self.update_speed(self.cruising_speed,self.cruising_speed)
        # Reverse drive
        elif key.name == "s":
            if self.cruising_speed <= 0 and not self.motor_control.dir:
                self.motor_control.change_direction(True,True)
            elif not self.motor_control.dir:
                self.cruising_speed -= 5
                self.update_speed(self.cruising_speed,self.cruising_speed)
            else:
                self.cruising_speed += 5
                self.update_speed(self.cruising_speed,self.cruising_speed)
        # E - Break
        elif key.name == "shift":
            self.cruising_speed = 10
            self.update_speed(self.cruising_speed,self.cruising_speed)
        # Capture an image  [spy mode]      
        elif key.name == "tab":
            self.camera.capture('images/spycam.jpg')
            detect_faces('images/spycam.jpg')
        # nitrous    
        elif key.name == "space":
            self.cruising_speed += 15
            self.update_speed(self.cruising_speed,self.cruising_speed)
        # Kill the program
        elif key.name == "delete":
            self.motor_control.end(0)
        # change to updated speed    
        self.motor_control.change_speed(self.lm_speed,self.rm_speed)


    def pid(self,ticks):
        """ Calculate new speed based on encoder data, target, and kp. 
        Used for for keeping motor stable
        """

        # The ticks that the encoders should be reading
        # TODO: make this dependent speed
        target_ticks = 2770
        # How much to update the speed based on  the errorerror
        kp = 0.0002

        # Calculate error
        la_error = target_ticks - ticks[0]
        lb_error = target_ticks - ticks[1]
        ra_error = target_ticks - ticks[2]
        rb_error = target_ticks - ticks[3]

        # Update the speed
        self.update_speed((la_error + lb_error) * kp, \
        (ra_error + rb_error) * kp)
     
        # Ensure speed is valid
        self.lm_speed = max(min(99, self.lm_speed), 0)
        self.rm_speed = max(min(99, self.rm_speed), 0)
        self.motor_control.change_speed(self.lm_speed,self.rm_speed)


    def update_speed(self,lm_speed,rm_speed):
        """ Utility function to update left and 
        right motors
        """

        if self.lm_speed > 99:
            print("LEFT MOTOR AT MAX SPEED")
        elif self.lm_speed < 0:
            print("LEFT MOTOR AT MIN SPEED")
        else:    
            self.lm_speed = lm_speed

        if self.rm_speed:
            print("RIGHT MOTOR AT MAX SPEED")
        elif self.rm_speed  < 0:
            print("RIGHT MOTOR AT MIN SPEED")
        else:
            self.rm_speed = rm_speed


    def bump_sensor_react(self,channel):
        """ Response for bump sensors bring hit
        """
        # start going backward
        self.motor_control.change_direction(True,True)
        sleep(.15)
        # Put right motor forward
        self.motor_control.change_direction(False,True)
        self.motor_control.change_speed(30,30)
        sleep(.15)
        self.motor_control.change_direction(True,False)
        assert self.motor_control.lm_dir == self.motor_control.rm_dir


    def turn_around(self):
        """ Utility function for robot doing a 180
        """

        # start going backward
        self.motor_control.change_direction(True,True)
        # increase spped to turn
        self.motor_control.change_speed(10,60)
        sleep(.75)
        # restore speed back
        self.motor_control.change_speed(self.cruising_speed,self.cruising_speed)
        self.motor_control.change_direction(0)

    def print_ticks(self,ticks):
        """ Utility print function to print out encoder data
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


    def add_interrupts(self):
        """ All the button sensors and encoder interrupts
        """
        # robot should reverse when it hits something
        GPIO.add_event_detect(C["BUTTON1"],GPIO.FALLING, callback = self.bump_sensor_react,bouncetime = 500)
        GPIO.add_event_detect(C["BUTTON3"],GPIO.FALLING, callback = self.bump_sensor_react,bouncetime = 200)
        GPIO.add_event_detect(C["BUTTON4"],GPIO.FALLING, callback = self.bump_sensor_react,bouncetime = 200)
        GPIO.add_event_detect(C["BUTTON5"],GPIO.FALLING, callback = self.bump_sensor_react,bouncetime = 200)
        GPIO.add_event_detect(C["BUTTON6"],GPIO.FALLING, callback = self.bump_sensor_react,bouncetime = 200)
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
 
        # Delays                
        SLEEP_TIME = 1
        # Give camera time to take image
        CAMERA_DELAY = 0.5
        SIGN_IMG = 'images/signs.jpg'
    
        while True:
            # FREE DRIVE /TELEOP MODE
            if self.drive_mode == 0 or self.drive_mode == 1:
                # Capture an image
                print("-----------------------------------")
                print(f"TAKING IMAGE AND SAVING TO {SIGN_IMG}")
                self.camera.capture(SIGN_IMG)
                sleep(CAMERA_DELAY)
                timer += CAMERA_DELAY
                # Check if any signs were found
                sign = detect_signs(SIGN_IMG)
                # Stop Sign
                if sign == 0:
                    print("STOP SIGN DETECTED")
                    self.motor_control.stop_motors()  
                # Yellow Sign    
                elif sign == 1:
                    print("YELLOW SIGN DETECTED")
                    self.update_speed(self.lm_speed-10,self.rm_speed-10)
                    self.motor_control.change_speed(self.lm_speed ,self.rm_speed)
                # Green Sign
                elif sign == 2:
                    print("GREEN SIGN DETECTED")
                    self.update_speed(self.lm_speed+10,self.rm_speed+10)
                    self.motor_control.change_speed(self.lm_speed ,self.rm_speed)
                else:
                    print("NO SIGNS DETECTED")
                print("-----------------------------------")
    
            # Calibrate encoders
            elif self.drive_mode == 3:
                self.calibrate_encoders()
          
            sleep(SLEEP_TIME)
            timer += SLEEP_TIME
            # REST ALL THE ECONDERS
            self.encoder.reset()

    
    


