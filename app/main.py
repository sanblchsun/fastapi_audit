from fastapi import FastAPI
from app.api import secrets, clients, health

app = FastAPI()

app.include_router(secrets.router, prefix="/api")
app.include_router(clients.router, prefix="/api")
app.include_router(health.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}
