# app/models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class ClientInfo(Base):
    __tablename__ = "client_info"

    id = Column(Integer, primary_key=True)
    hostname = Column(String, nullable=False)
    username = Column(String, nullable=False)
    os = Column(String, nullable=False)
    cpu = Column(String)
    ram_gb = Column(String)
    ip_address = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
