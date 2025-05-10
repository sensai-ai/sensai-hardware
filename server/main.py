import os
import sys

import uvicorn
from fastapi import FastAPI

from server.api.temperature import router as temperature_router
from server.api.relay import router as relay_router

app = FastAPI()

# Mount the imported router directly to the app
app.include_router(router=temperature_router, prefix="/temperature", tags=["Temperature"])
app.include_router(router=relay_router, prefix="/relay", tags=["Relay"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
