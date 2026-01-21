from fastapi import APIRouter, Depends, Header, HTTPException, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import ClientInfo
from app.defs.client_ip import get_client_ip
from app.config import settings

router = APIRouter()


@router.post("/clients/register")
async def register_client(
    data: dict,
    request: Request,
    x_api_token: str = Header(...),
    session: AsyncSession = Depends(get_db),
):
    if x_api_token != settings.SECRET_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

    result = await session.execute(
        select(ClientInfo).where(
            ClientInfo.hostname == data["hostname"],
            ClientInfo.username == data["username"],
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        return {"status": "already_registered"}

    client = ClientInfo(
        hostname=str(data["hostname"]),
        username=str(data["username"]),
        os=str(data["os"]),
        cpu=str(data.get("cpu")) if data.get("cpu") else None,
        ram_gb=str(data.get("ram_gb")) if data.get("ram_gb") else None,
        internal_ip=str(data.get("internal_ip")) if data.get("internal_ip") else None,
        external_ip=str(get_client_ip(request)),  # IP, с которого пришел запрос
    )

    session.add(client)
    await session.commit()

    return {"status": "ok"}
