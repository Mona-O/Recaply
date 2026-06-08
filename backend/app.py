from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from alembic.config import Config as AlembicConfig
from alembic import command as alembic_command

from routers.report_router import router as report_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    print("Application des migrations Alembic...")
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_command.upgrade(alembic_cfg, "head")
    print(" Migrations appliquées")
    
    yield  # l'app tourne ici
    
    print("Arrêt du serveur")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(report_router)