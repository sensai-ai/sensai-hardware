"""
Temperature Database Module

This module provides functionality to store and manage temperature readings in the database.
It includes functions for storing temperature data and verifying the stored values.
"""

import logging
from typing import Optional

from supabase import Client

# Import the model from your models directory
from server.models.Temperature import TemperatureReading

logger = logging.getLogger(__name__)


def store_temperature(
    supabase: Client, temp_c: float, temp_f: float
) -> Optional[TemperatureReading]:
    """
    Store the temperature data in Supabase and verify the insertion.

    Args:
        supabase (Client): Supabase client instance
        temp_c (float): Temperature in Celsius
        temp_f (float): Temperature in Fahrenheit

    Returns:
        Optional[TemperatureReading]: The stored temperature reading if successful, None otherwise
    """
    try:
        data = {"celsius": temp_c, "fahrenheit": temp_f}
        response = supabase.table("temperature_readings").insert(data).execute()
        if hasattr(response, "data") and len(response.data) > 0:
            inserted_data = response.data[0]
            validated_data = TemperatureReading(**inserted_data)
            if (
                abs(validated_data.celsius - temp_c) < 0.01
                and abs(validated_data.fahrenheit - temp_f) < 0.01
            ):
                logger.info(
                    f"Stored and verified temperature in Supabase: {validated_data.model_dump()}"
                )
                return validated_data
            else:
                logger.error(
                    f"Data verification failed. Expected ({temp_c}, {temp_f}), "
                    f"got ({validated_data.celsius}, {validated_data.fahrenheit})"
                )
                return None
        else:
            logger.error("Failed to insert temperature data: No data returned")
            return None
    except Exception as e:
        logger.error(f"Failed to store temperature in Supabase: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    from supabase import create_client

    # Initialize Supabase client (you'll need to provide your own credentials)
    supabase_url = "YOUR_SUPABASE_URL"
    supabase_key = "YOUR_SUPABASE_KEY"
    supabase = create_client(supabase_url, supabase_key)

    # Example temperature reading
    temp_c = 25.5
    temp_f = 77.9

    # Store the temperature
    result = store_temperature(supabase, temp_c, temp_f)
    if result:
        print(f"Successfully stored temperature: {result.model_dump()}")
    else:
        print("Failed to store temperature")
