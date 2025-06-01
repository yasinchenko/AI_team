# worker.py
import asyncio
import asyncpg
from redis.asyncio import Redis

DB_URL = "postgresql://user:pass@db:5432/taskrouter"
REDIS_URL = "redis://redis:6379"

async def process_task(task_id, db):
    async with db.acquire() as conn:
        task = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
        print(f"[WORKER] Processing task {task_id}: {task['title']}")
        await conn.execute("UPDATE tasks SET state = 'assigned' WHERE id = $1", task_id)

async def main():
    redis = Redis.from_url(REDIS_URL, decode_responses=True)
    db = await asyncpg.create_pool(DB_URL)
    print("[WORKER] Started. Waiting for tasks...")
    while True:
        task_id = await redis.brpop("task_queue", timeout=0)
        if task_id:
            _, task_value = task_id
            await process_task(task_value, db)
            print(f"[WORKER] Task {task_value} processed.")

if __name__ == "__main__":
    asyncio.run(main())