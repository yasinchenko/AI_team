# app/core/lifecycle.py
from app.db.database import connect, disconnect

async def startup():
    await connect()

async def shutdown():
    await disconnect()