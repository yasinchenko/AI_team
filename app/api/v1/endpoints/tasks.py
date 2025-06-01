# app/api/v1/endpoints/tasks.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from uuid import uuid4
from asyncpg import Pool
from redis.asyncio import Redis
from app.db.database import get_db, get_redis
from app.db.fsm import get_next_state

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 3
    depends_on: Optional[List[str]] = []

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    priority: int
    state: str
    depends_on: List[str]
    generated_code: Optional[str] = None

@router.post("/", response_model=Task)
async def create_task(task: TaskCreate, db: Pool = Depends(get_db), redis: Redis = Depends(get_redis)):
    task_id = str(uuid4())
    async with db.acquire() as conn:
        await conn.execute("""
            INSERT INTO tasks (id, title, description, priority, state, depends_on)
            VALUES ($1, $2, $3, $4, 'created', $5)
        """, task_id, task.title, task.description, task.priority, task.depends_on)
    await redis.lpush("task_queue", task_id)
    return Task(id=task_id, title=task.title, description=task.description,
                priority=task.priority, state="created", depends_on=task.depends_on)

@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str, db: Pool = Depends(get_db)):
    async with db.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
        return Task(**row)

@router.post("/{task_id}/advance")
async def advance_task(task_id: str, db: Pool = Depends(get_db)):
    async with db.acquire() as conn:
        row = await conn.fetchrow("SELECT state FROM tasks WHERE id = $1", task_id)
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
        current_state = row["state"]
        try:
            next_state = get_next_state(current_state)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        await conn.execute("UPDATE tasks SET state = $1 WHERE id = $2", next_state, task_id)
        return {"task_id": task_id, "new_state": next_state}
