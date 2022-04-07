

from driver import Driver
from pin_setup import setup
# Configure all the pins
setup()
if __name__ == "__main__":
    drive_mode = input("[1] for teleop, [0] for freeroam: ")
    crusing_speed = input("enter default cruising speed: ")

    driver = Driver(drive_mode,crusing_speed)
    driver.drive()
    