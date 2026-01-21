from pydantic import BaseModel


class ClientInfoIn(BaseModel):
    hostname: str
    username: str
    os: str
    cpu: str | None = None
    ram_gb: str | None = None
    ip_internal: str | None = None
    ip_external: str | None = None
