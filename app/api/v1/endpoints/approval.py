# app/api/v1/endpoints/approval.py
from fastapi import APIRouter, Depends, HTTPException
from asyncpg import Pool
from app.db.database import get_db

router = APIRouter()

@router.post("/{task_id}/approve")
async def approve_task(task_id: str, db: Pool = Depends(get_db)):
    async with db.acquire() as conn:
        result = await conn.execute(
            "UPDATE tasks SET state = 'approved' WHERE id = $1 AND state = 'waiting_approval'",
            task_id
        )
        if result == "UPDATE 0":
            raise HTTPException(status_code=400, detail="Task not in waiting_approval state")
        return {"task_id": task_id, "new_state": "approved"}
