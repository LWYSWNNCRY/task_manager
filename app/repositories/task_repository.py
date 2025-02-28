from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(Task))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, task_id: int):
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            raise NoResultFound()
        return task

    @staticmethod
    async def create(db: AsyncSession, task_data: TaskCreate):
        task = Task(**task_data.model_dump())
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def update(db: AsyncSession, task_id: int, task_data: TaskUpdate):
        task = await TaskRepository.get_by_id(db, task_id)
        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def delete(db: AsyncSession, task_id: int):
        task = await TaskRepository.get_by_id(db, task_id)
        await db.delete(task)
        await db.commit()
