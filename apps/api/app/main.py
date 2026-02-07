#apps/api/app/main.py
from __future__ import annotations

"""
Application entry point for the BGG Shelf Mapper API

This module is responsible for:
- Creating the FastAPI app
- Wiring middleware (CORS)
- Initializing database tables
- Seeding sample data for local/dev usage
- Registering all API routers

It intentionally does NOT:
- Contain business logic
- Handle request validation
- Know anything about BGG internals
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import engine, SessionLocal
from .models import Base
from .seed import seed_if_empty

# Route modules (explicit imports make wiring obvious)
from .routes.games import router as games_router
from .routes.fixtures import router as fixtures_router
from .routes.placements import router as placements_router
from .routes.sync import router as sync_router


# -----------------------------------------------------------------------------
# FastAPI app configuration
# -----------------------------------------------------------------------------

app = FastAPI(
    title="BGG Shelf Mapper API",
    version="0.1.0",
)


# -----------------------------------------------------------------------------
# Middleware
# -----------------------------------------------------------------------------
# Development-friendly CORS configuration
# This allows the Vite dev server to call the API during local development
# Can tighten this if/when the API is exposed publicly

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


# -----------------------------------------------------------------------------
# Application lifecycle
# -----------------------------------------------------------------------------

@app.on_event("startup")
def on_startup() -> None:
    """
    Application startup hook

    Responsibilities:
    - Create database tables if they do not exist
    - Seed sample data (fixtures, games, placements) ONLY if DB is empty

    Notes:
    - This runs in normal app startup (Docker, uvicorn)
    - Tests override the DB dependency and do NOT rely on this hook
    """
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        seed_if_empty(db)


# -----------------------------------------------------------------------------
# Health check
# -----------------------------------------------------------------------------

@app.get("/api/health")
def health() -> dict:
    """
    Simple health check endpoint

    Useful for:
    - Docker readiness checks
    - Quick sanity testing
    """
    return {"ok": True}


# -----------------------------------------------------------------------------
# API routes
# -----------------------------------------------------------------------------
# Each router owns a specific domain and URL space
# Explicit includes avoid "why is this 404?" debugging

app.include_router(games_router)
app.include_router(fixtures_router)
app.include_router(placements_router)
app.include_router(sync_router)
