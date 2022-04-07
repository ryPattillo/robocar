

from driver import Driver
from pin_setup import setup
# Configure all the pins
setup()
if __name__ == "__main__":
    driver = Driver()
    drive_mode = input("[1] for teleop, [0] for freeroam")
    driver.main(drive_mode)
    