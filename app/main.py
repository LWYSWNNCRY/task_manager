from fastapi import FastAPI
from app.api.routers.tasks import router as task_router

app = FastAPI(title="Task Manager API")

app.include_router(task_router)
