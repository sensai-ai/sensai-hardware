import os
import sys

import uvicorn
from fastapi import FastAPI

from server.api.temperature import router as temperature_router

app = FastAPI()

# Mount the imported router directly to the app
app.include_router(router=temperature_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
