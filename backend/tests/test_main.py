# tests/test_main.py
import pytest
from sqlalchemy.orm import Session
from src import crud  # Import your CRUD functions

def test_create_user(client, db_session: Session):
    # Example test data
    user_data = {"name": "Test User", "email": "testuser@example.com"}

    # Make a POST request to create a user
    response = client.post("/users/", json=user_data)

    # Assertions to verify response status and data
    assert response.status_code == 200
    assert response.json()["name"] == user_data["name"]

    # Check the user was added to the database using the CRUD function
    user_in_db = crud.get_user(db_session, response.json()["id"])
    assert user_in_db.email == user_data["email"]

def test_read_user(client, db_session: Session):
    # Create a user directly in the test database
    user = crud.create_user(db_session, name="Read Test", email="readtest@example.com")

    # Test fetching the user by ID
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["email"] == "readtest@example.com"
