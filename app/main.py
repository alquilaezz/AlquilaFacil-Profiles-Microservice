from fastapi import FastAPI
from .database import Base, engine
from .routers import profiles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Profiles Service")

app.include_router(profiles.router)
