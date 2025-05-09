from fastapi import FastAPI

# from server.api.endpoints.ds18b20 import router as ds18b20_router
from server.api.relay import router as relay_router

app = FastAPI()
# app.include_router(ds18b20_router)
app.include_router(relay_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
