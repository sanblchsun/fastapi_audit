from fastapi import APIRouter, Depends, Header, HTTPException, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import ClientInfo
from app.defs.client_ip import get_client_ips
from app.config import settings

router = APIRouter()


# ===========================
# POST /clients/register
# ===========================
@router.post("/clients/register")
async def register_client(
    data: dict,
    request: Request,
    x_api_token: str = Header(...),
    session: AsyncSession = Depends(get_db),
):
    if x_api_token != settings.SECRET_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Проверка, есть ли уже клиент в базе
    result = await session.execute(
        select(ClientInfo).where(
            ClientInfo.hostname == data["hostname"],
            ClientInfo.username == data["username"],
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        return {"status": "already_registered"}

    # Получаем оба IP
    ip_internal, ip_external = get_client_ips(request)

    client = ClientInfo(
        hostname=data["hostname"],
        username=data["username"],
        os=data["os"],
        cpu=data.get("cpu"),
        ram_gb=data.get("ram_gb"),
        internal_ip=ip_internal,  # Локальный IP
        external_ip=ip_external,  # Внешний IP
    )

    session.add(client)
    await session.commit()

    return {"status": "ok"}
