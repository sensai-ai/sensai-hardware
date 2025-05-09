from typing import Optional

from fastapi import APIRouter, FastAPI, HTTPException, status
from pydantic import BaseModel

from server.services.relay_controller import control_relay
from server.services.utils import get_logger

router = APIRouter(prefix="/relay", tags=["Relay"])


class RelayState(BaseModel):
    state: bool

    class Config:
        schema_extra = {"example": {"state": False}}


@router.post("/", response_model=dict)
async def set_relay_state(relay_state: RelayState):
    """
    Turn the relay ON (state: true) or OFF (state: false).
    Returns success status, message, and current state.
    """
    control_relay(False)  # Ensure the relay is off at startup
    result = control_relay(relay_state.state)

    if not result["status"]:
        raise HTTPException(status_code=500, detail=result["message"])

    return result
