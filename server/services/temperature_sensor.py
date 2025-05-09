"""
Temperature Sensor Module

This module provides functionality to read temperature data from a DS18B20 temperature sensor
connected to a Raspberry Pi. It includes functions to locate the sensor, read raw data,
and process the temperature readings in both Celsius and Fahrenheit.
"""

import glob
import logging
import time

logger = logging.getLogger(__name__)


def _locate_ds18b20_device() -> str | None:
    """
    Locate the DS18B20 sensor device file.

    Returns:
        str | None: Path to the device file if found, None otherwise
    """
    base_dir = "/sys/bus/w1/devices/"
    try:
        device_folder = glob.glob(base_dir + "28*")[0]
        device_file = device_folder + "/w1_slave"
        return device_file
    except IndexError:
        logger.error("No DS18B20 device found")
        return None


def _read_temp_raw() -> list[str]:
    """
    Read raw data from the sensor's w1_slave file.

    Returns:
        list[str]: Raw lines from the sensor file

    Raises:
        Exception: If temperature sensor is not found
    """
    device_file = _locate_ds18b20_device()
    if device_file is None:
        raise Exception("Temperature sensor not found")
    with open(device_file, "r") as f:
        lines = f.readlines()
    return lines


def read_temp() -> tuple[float, float]:
    """
    Process raw data to extract temperature in Celsius and Fahrenheit.

    Returns:
        tuple[float, float]: Temperature in Celsius and Fahrenheit

    Raises:
        Exception: If temperature data is invalid
    """
    lines = _read_temp_raw()
    while lines[0].strip()[-3:] != "YES":  # Wait for a valid reading
        time.sleep(0.2)
        lines = _read_temp_raw()
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2 :]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        logger.info(f"Temperature: {temp_c:.2f}°C / {temp_f:.2f}°F")
        return round(temp_c, 2), round(temp_f, 2)
    else:
        logger.error("Invalid temperature data")
        raise Exception("Invalid temperature data")


if __name__ == "__main__":
    # Example usage
    try:
        temp_c, temp_f = read_temp()
        print(f"Temperature: {temp_c}°C / {temp_f}°F")
    except Exception as e:
        print(f"Error reading temperature: {e}")
