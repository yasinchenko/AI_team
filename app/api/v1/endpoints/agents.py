# app/api/v1/endpoints/agents.py
from fastapi import APIRouter, Depends, HTTPException
from asyncpg import Pool
from app.db.database import get_db
from app.services.dispatcher import route_task_to_agent

router = APIRouter()

@router.post("/{task_id}/generate")
async def generate_code(task_id: str, db: Pool = Depends(get_db)):
    async with db.acquire() as conn:
        task = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        result = await route_task_to_agent(dict(task))
        await conn.execute(
            "UPDATE tasks SET generated_code = $1 WHERE id = $2",
            result, task_id
        )
        return {"task_id": task_id, "result": result}