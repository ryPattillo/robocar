""" Main module to be run to start the robot
"""
from driver import Driver
from pin_setup import setup

if __name__ == "__main__":
    setup()
    drive_mode = int(input("[0] for freeroam, [1] for teleop, [2] for  encoder calibration: "))
    if not (drive_mode == 2):
        cruising_speed = float(input("Enter starting speed: "))
    driver = Driver(drive_mode,cruising_speed)
    driver.drive()
    