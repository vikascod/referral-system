from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
import pytest
from fastapi.testclient import TestClient
from app.main import app


URL = 'sqlite:///test.db'

engine = create_engine(URL, connect_args={'check_same_thread':False})

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture(scope="module")
def session():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client(session):
    def test_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = test_get_db
    yield TestClient(app)