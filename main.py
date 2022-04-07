

from driver import Driver
from pin_setup import setup
# Configure all the pins
setup()
if __name__ == "__main__":
    drive_mode = int(input("[0] for freeroam, [1] for teleop: "))
    cruising_speed = float(input("enter default cruising speed: "))
    driver = Driver(drive_mode,cruising_speed)
    driver.drive()
    