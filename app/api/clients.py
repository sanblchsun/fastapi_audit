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
        hostname=data["hostname"],
        username=data["username"],
        os=data["os"],
        cpu=data.get("cpu"),
        ram_gb=data.get("ram_gb"),
        ip_address=get_client_ip(request),
    )

    session.add(client)
    await session.commit()

    return {"status": "ok"}
