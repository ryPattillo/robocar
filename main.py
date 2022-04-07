

from driver import Driver
from pin_setup import setup
# Configure all the pins
setup()
if __name__ == "__main__":
    drive_mode = int(input("[0] for teleop, [1] for freeroam: "))
    if drive_mode == 1:
        cruising_speed = float(input("enter default cruising speed: "))
    driver = Driver(drive_mode,cruising_speed)
    driver.drive()
    