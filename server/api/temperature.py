from fastapi import APIRouter, HTTPException, status

from server.db.supabase_client import SupabaseClientManager
from server.models.Temperature import (SQLQueryRequest, SQLQueryResponse,
                                       TemperatureReading)
from server.services.utils import get_logger
from server.services.temperature_sensor import read_temp

logger = get_logger(__name__)

# Initialize API Router
router = APIRouter(prefix="/temperature", tags=["Temperature"])

# Initialize Supabase client
supabase = SupabaseClientManager().get_client()


@router.get("/", response_model=TemperatureReading, status_code=status.HTTP_200_OK)
async def read_temperature():
    """Endpoint to return the most recent stored temperature."""
    recent_reading = read_temp()
    if recent_reading:
        temperature_data = TemperatureReading(
            celsius=recent_reading[0], fahrenheit=recent_reading[1]  # temp_c  # temp_f
        )
        logger.info(f"Returning recent temperature: {temperature_data.model_dump()}")
        return temperature_data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No temperature readings available",
        )
