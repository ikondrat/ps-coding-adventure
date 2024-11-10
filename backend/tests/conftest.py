# tests/conftest.py
import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))


from main import app  # Import your FastAPI app
from database import Base

# Set the TESTING environment variable
os.environ["TESTING"] = "True"

# Use the test database URL
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the database dependency to use the test database session
@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)  # Create tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Clean up the test database

# Create a fixture for the FastAPI test client
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
