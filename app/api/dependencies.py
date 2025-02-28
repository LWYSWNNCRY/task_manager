from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db


async def get_db_session(db: AsyncSession = Depends(get_db)):
    """Dependency function to retrieve a database session."""
    return db
