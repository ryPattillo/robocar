

from driver import Driver
from pin_setup import setup
# Configure all the pins
setup()
if __name__ == "__main__":
    drive_mode = int(input("[0] for freeroam, [1] for teleop, [2] for instructed, \
        [3] for testing: "))
    if not (drive_mode == 2 or drive_mode == 3):
        cruising_speed = float(input("Enter starting speed: "))
    driver = Driver(drive_mode,cruising_speed)
    driver.drive()
    