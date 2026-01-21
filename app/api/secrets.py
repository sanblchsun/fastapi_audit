from fastapi import APIRouter, Header, HTTPException
from app.config import settings

router = APIRouter()


@router.post("/secrets/get")
def get_secret(key: str, x_api_token: str = Header(...)):
    """
    Получение логина/пароля администратора.
    """
    if x_api_token != settings.SECRET_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

    secrets = {
        "admin_username": settings.FIRST_SUPERUSER,
        "admin_password": settings.FIRST_SUPERUSER_PASSWORD,
    }

    if key not in secrets:
        raise HTTPException(status_code=404, detail="Secret not found")

    return {"value": secrets[key]}
