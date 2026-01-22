from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import Depends

from app.database import get_db

router = APIRouter()


@router.get("/health")
async def health(session: AsyncSession = Depends(get_db)):
    # проверяем, что БД жива
    await session.execute(text("SELECT 1"))
    return {"status": "ok"}
