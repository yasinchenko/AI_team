# app/api/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import tasks, agents, approval

router = APIRouter()

router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
router.include_router(agents.router, prefix="/agents", tags=["agents"])
router.include_router(approval.router, prefix="/approval", tags=["approval"])