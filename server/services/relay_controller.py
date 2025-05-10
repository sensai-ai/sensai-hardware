"""
Relay Controller Module

This module provides functionality to control a relay connected to a Raspberry Pi's GPIO pins.
It includes a monkey patch for lgpio compatibility with Raspberry Pi 5 and a function to control
the relay state.
"""

from time import sleep

import gpiozero.pins.lgpio
import lgpio
from gpiozero import OutputDevice


# Monkey patch for lgpio on Raspberry Pi 5
def __patched_init(self, chip=None):
    gpiozero.pins.lgpio.LGPIOFactory.__bases__[0].__init__(self)
    chip = 0
    self._handle = lgpio.gpiochip_open(chip)
    self._chip = chip
    self.pin_class = gpiozero.pins.lgpio.LGPIOPin


gpiozero.pins.lgpio.LGPIOFactory.__init__ = __patched_init


# Define the relay pin (GPIO 17, Pin 11)
RELAY_PIN = 17
relay = OutputDevice(
    RELAY_PIN,
    active_high=False,
    initial_value=False,
    pin_factory=gpiozero.pins.lgpio.LGPIOFactory(),
)
relay.off()  # Ensure the relay is off at startup


def control_relay(state: bool) -> dict:
    """
    Control the relay state (ON or OFF).

    Args:
        state (bool): True to turn the relay ON, False to turn it OFF.

    Returns:
        dict: A dictionary containing the status of the operation.
              Example: {"status": "success", "state": "ON"}
                       or {"status": "error", "message": "Error description"}
    """
    try:
        if state:
            relay.off()  # Sets GPIO LOW for active-low relay
            return {"status": "success", "state": "ON"}
        else:
            relay.on()  # Sets GPIO HIGH for active-low relay
            return {"status": "success", "state": "OFF"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    # Example usage
    result = control_relay(True)
    print(f"Relay {result['state']}: {result['status']}")
    sleep(2)
    result = control_relay(False)
    print(f"Relay {result['state']}: {result['status']}")
    sleep(2)
