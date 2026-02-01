from __future__ import annotations

import os
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # loads repo-root .env if present


def _db_url() -> str:
    data_dir = os.getenv("API_DATA_DIR", "./data")
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{Path(data_dir) / 'app.db'}"


engine = create_engine(
    _db_url(),
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
