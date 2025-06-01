# app/db/database.py (обновить подключение через settings)
import asyncpg
from redis.asyncio import Redis
from fastapi import Depends
from app.core.config import settings

DB_URL = settings.DATABASE_URL
REDIS_URL = settings.REDIS_URL

pg_pool: asyncpg.Pool = None
redis_client: Redis = None

async def connect():
    global pg_pool, redis_client
    pg_pool = await asyncpg.create_pool(dsn=DB_URL)
    redis_client = Redis.from_url(REDIS_URL, decode_responses=True)
    async with pg_pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            priority INT,
            state TEXT,
            depends_on TEXT[],
            generated_code TEXT
        )
        """)

async def disconnect():
    await pg_pool.close()
    await redis_client.close()

def get_db() -> asyncpg.Pool:
    return pg_pool

def get_redis() -> Redis:
    return redis_client