from fastapi import APIRouter
from pydantic import BaseModel
from src.orchestration.router import TaskRouter

router = APIRouter()
task_router = TaskRouter()

class TaskRequest(BaseModel):
    scenario: str
    payload: dict

@router.post("/execute")
async def execute_task(request: TaskRequest):
    """
    Entry point for external requests.
    Passes the payload to the deterministic Orchestration Layer.
    """
    result = await task_router.route_task(request.scenario, request.payload)
    return {"status": "success", "data": result}