import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://dogs_user:dogs_password@localhost:5434/dogs_test_db",
)

engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Create tables once for the whole test session.
    (Assumes Alembic has your schema, but this is fine for tests.)
    """
    Base.metadata.create_all(bind=engine)
    yield
    # Optional: drop all tables at end
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def clean_tables():
    """
    Clean data before each test so tests are isolated.
    """
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE dogs RESTART IDENTITY CASCADE;"))
        conn.commit()
    yield


@pytest.fixture()
def client():
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
