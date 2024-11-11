import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from main import app, get_session

test_uuid = "123e4567-e89b-12d3-a456-426614174000"


@pytest.fixture(scope="module")
def test_create_board(test_client):
    client = test_client

    # Validate what there is no boards and users
    assert len(client.get("/boards/").json()) == 0
    assert len(client.get("/users/").json()) == 0

    # Create a user
    client.post("/users/", json={"name": "Deadpond", "id": test_uuid})
    assert len(client.get("/users/").json()) == 1

    # Create a board
    response = client.post("/boards/", json={"name": "Board 1", "user_id": test_uuid})
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Board 1"
    assert data["id"] is not None
    assert data["access_key"] is not None
    assert data["user_id"] == test_uuid

    assert len(client.get("/boards/").json()) == 1

    # Delete the user and validate that the board was deleted by cascading deletion
    client.delete(f"/users/{test_uuid}")
    assert len(client.get("/users/").json()) == 0
    assert len(client.get("/boards/").json()) == 0
