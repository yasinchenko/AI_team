# main.py
from fastapi import FastAPI
from app.api.v1.router import router
from app.core.lifecycle import startup, shutdown

app = FastAPI(title="TaskRouter AI")

@app.on_event("startup")
async def on_startup():
    await startup()

@app.on_event("shutdown")
async def on_shutdown():
    await shutdown()

app.include_router(router, prefix="/api/v1")
