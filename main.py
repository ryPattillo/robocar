

from driver import Driver
import keyboard
from pin_setup import setup

# Configure all the pins
setup()

if __name__ == "__main__":
    driver = Driver()
    driver.main()
   