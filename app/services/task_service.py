from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:

    @staticmethod
    async def get_all_tasks(db: AsyncSession):
        return await TaskRepository.get_all(db)

    @staticmethod
    async def get_task_by_id(db: AsyncSession, task_id: int):
        try:
            return await TaskRepository.get_by_id(db, task_id)
        except NoResultFound:
            return None

    @staticmethod
    async def create_task(db: AsyncSession, task_data: TaskCreate):
        return await TaskRepository.create(db, task_data)

    @staticmethod
    async def update_task(db: AsyncSession, task_id: int, task_data: TaskUpdate):
        try:
            return await TaskRepository.update(db, task_id, task_data)
        except NoResultFound:
            return None

    @staticmethod
    async def delete_task(db: AsyncSession, task_id: int):
        try:
            await TaskRepository.delete(db, task_id)
            return True
        except NoResultFound:
            return False
