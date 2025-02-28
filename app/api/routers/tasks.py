from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db_session
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()


@router.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(db: AsyncSession = Depends(get_db_session)) -> list[TaskResponse]:
    return await TaskService.get_all_tasks(db)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db_session)) -> TaskResponse:
    task = await TaskService.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/tasks", response_model=TaskResponse)
async def create_task(task_data: TaskCreate, db: AsyncSession = Depends(get_db_session)) -> TaskResponse:
    return await TaskService.create_task(db, task_data)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_data: TaskUpdate, db: AsyncSession = Depends(get_db_session)) -> TaskResponse:
    task = await TaskService.update_task(db, task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    success = await TaskService.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}
