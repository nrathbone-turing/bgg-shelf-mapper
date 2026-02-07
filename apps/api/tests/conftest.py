#apps/api/tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db import get_db
from app.models import Base, Game, Fixture, Placement

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def seed_test_data(db):
    #Fixture
    fixture = Fixture(name="Office Cubes (2x5)", rows=2, cols=5)
    db.add(fixture)
    db.flush()

    #Games
    games = [
        Game(bgg_id=68448, name="7 Wonders", year_published=2010),
        Game(bgg_id=199042, name="Harry Potter: Hogwarts Battle", year_published=2016),
        Game(bgg_id=206931, name="Encore!", year_published=2016),
        Game(bgg_id=40692, name="Small World", year_published=2009),
        Game(bgg_id=92415, name="Skull", year_published=2011),
        Game(bgg_id=204583, name="Kingdomino", year_published=2016),
    ]
    db.add_all(games)
    db.flush()

    #Placements
    for i, game in enumerate(games[:5]):
        db.add(Placement(fixture_id=fixture.id, slot=f"r0c{i}", game_id=game.id))

    db.add(Placement(fixture_id=fixture.id, slot="r1c0", game_id=games[5].id))
    db.commit()


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        seed_test_data(db)
    finally:
        db.close()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
