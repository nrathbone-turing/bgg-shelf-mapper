from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import engine, SessionLocal
from .models import Base
from .seed import seed_if_empty
from .routes.games import router as games_router
from .routes.fixtures import router as fixtures_router
from .routes.placements import router as placements_router
from .routes.sync import router as sync_router


app = FastAPI(title="BGG Shelf Mapper API", version="0.1.0")

# Dev-friendly CORS (tighten later if you expose this beyond localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    # Create tables and seed sample data (only if DB is empty)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_if_empty(db)


@app.get("/api/health")
def health() -> dict:
    return {"ok": True}


# API routes
app.include_router(games_router)
app.include_router(fixtures_router)
app.include_router(placements_router)
app.include_router(sync_router)
