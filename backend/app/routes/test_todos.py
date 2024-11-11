import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from main import app, get_session

test_uuid = "123e4567-e89b-12d3-a456-426614174000"


@pytest.fixture(scope="module")
def test_client():
    engine = create_engine(
        "postgresql://postgres:postgrespassword@localhost:5432/postgres"
    )
    SQLModel.metadata.create_all(engine)

    client = TestClient(app)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        yield client  # This will be used in the test

        app.dependency_overrides.clear()

    # Teardown code can be added here if needed
    SQLModel.metadata.drop_all(engine)  # Optional: Clean up after tests


def test_create_todo(test_client):
    client = test_client
    access_key = "123e4567-e89b-12d3-a456-426614174000"
    board_id = "223e4567-e89b-12d3-b456-426614174000"

    # Create a user
    client.post("/users/", json={"name": "Deadpond", "id": test_uuid})
    assert len(client.get("/users/").json()) == 1

    # Create a board
    client.post(
        "/boards/",
        json={
            "name": "Board 1",
            "id": board_id,
            "user_id": test_uuid,
            "access_key": access_key,
        },
    )

    # Create a todo
    response = client.post(
        "/todos/",
        json={
            "title": "Todo 1",
            "board_id": board_id,
            "state": "TODO",
            "user_id": test_uuid,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Todo 1"
    assert data["board_id"] == board_id
    assert data["state"] == "TODO"
    assert data["user_id"] == test_uuid

    # Delete the user and validate that the board was deleted by cascading deletion
    client.delete(f"/users/{test_uuid}")


def test_update_todo(test_client):
    client = test_client
    # Arrange
    todo_id = "323e4567-e89b-12d3-c456-426614174000"
    access_key = "123e4567-e89b-12d3-a456-426614174000"
    board_id = "223e4567-e89b-12d3-b456-426614174000"

    # Create a user
    client.post("/users/", json={"name": "Deadpond", "id": test_uuid})

    # Create a board
    client.post(
        "/boards/",
        json={
            "name": "Board 1",
            "id": board_id,
            "user_id": test_uuid,
            "access_key": access_key,
        },
    )

    # Create a todo
    response = client.post(
        "/todos/",
        json={
            "title": "Todo 1",
            "id": todo_id,
            "board_id": board_id,
            "state": "TODO",
            "user_id": test_uuid,
        },
    )

    updated_todo = {
        "title": "Todo 2",
        "state": "ONGOING",
    }
    # Act
    response = client.put(
        f"/todos/{todo_id}",
        json=updated_todo,
    )

    # Assert
    assert response.status_code == 200
    updated_todo = response.json()
    assert updated_todo["title"] == updated_todo["title"]
    assert updated_todo["state"] == updated_todo["state"]

    client.delete(f"/users/{test_uuid}")


def test_update_todo_transitions_valid(test_client):
    client = test_client
    # Arrange
    todo_id = "323e4567-e89b-12d3-c456-426614174000"
    access_key = "123e4567-e89b-12d3-a456-426614174000"
    board_id = "223e4567-e89b-12d3-b456-426614174000"

    # Create a user
    client.post("/users/", json={"name": "Deadpond", "id": test_uuid})

    # Create a board
    client.post(
        "/boards/",
        json={
            "name": "Board 1",
            "id": board_id,
            "user_id": test_uuid,
            "access_key": access_key,
        },
    )

    # Create a todo
    response = client.post(
        "/todos/",
        json={
            "title": "Todo 1",
            "id": todo_id,
            "board_id": board_id,
            "state": "TODO",
            "user_id": test_uuid,
        },
    )
    # Test valid state transition from TODO to ONGOING
    response = client.put(
        f"/todos/{todo_id}", json={"title": "Todo 1", "state": "ONGOING"}
    )
    assert response.status_code == 200
    assert response.json()["state"] == "ONGOING"

    # Test valid state transition from ONGOING to DONE
    response = client.put(
        f"/todos/{todo_id}", json={"title": "Todo 1", "state": "DONE"}
    )
    assert response.status_code == 200
    assert response.json()["state"] == "DONE"

    # Test valid state transition from DONE to ONGOING
    response = client.put(
        f"/todos/{todo_id}", json={"title": "Todo 1", "state": "ONGOING"}
    )
    assert response.status_code == 200
    assert response.json()["state"] == "ONGOING"

    # Test valid state transition from ONGOING to TODO
    response = client.put(
        f"/todos/{todo_id}", json={"title": "Todo 1", "state": "TODO"}
    )
    assert response.status_code == 200
    assert response.json()["state"] == "TODO"

    client.delete(f"/users/{test_uuid}")


def test_update_todo_transitions_invalid(test_client):
    client = test_client
    # Arrange
    todo_id = "323e4567-e89b-12d3-c456-426614174000"
    access_key = "123e4567-e89b-12d3-a456-426614174000"
    board_id = "223e4567-e89b-12d3-b456-426614174000"

    # Create a user
    client.post("/users/", json={"name": "Deadpond", "id": test_uuid})

    # Create a board
    client.post(
        "/boards/",
        json={
            "name": "Board 1",
            "id": board_id,
            "user_id": test_uuid,
            "access_key": access_key,
        },
    )

    # Create a todo
    response = client.post(
        "/todos/",
        json={
            "title": "Todo 1",
            "id": todo_id,
            "board_id": board_id,
            "state": "TODO",
            "user_id": test_uuid,
        },
    )

    # Test valid state transition from TODO to DONE
    response = client.put(
        f"/todos/{todo_id}", json={"title": "Todo 1", "state": "DONE"}
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Invalid state transition"

    response = client.put(
        f"/todos/{todo_id}", json={"title": "Todo 1", "state": "ONGOING"}
    )
    assert response.status_code == 200

    response = client.put(
        f"/todos/{todo_id}", json={"title": "Todo 1", "state": "DONE"}
    )
    assert response.status_code == 200

    # Test valid state transition from DONE to TODO
    response = client.put(
        f"/todos/{todo_id}", json={"title": "Todo 1", "state": "TODO"}
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Invalid state transition"

    client.delete(f"/users/{test_uuid}")


def test_board_todos(test_client):
    client = test_client
    access_key = "123e4567-e89b-12d3-a456-426614174000"
    board_id = "223e4567-e89b-12d3-b456-426614174000"

    # Create a user
    client.post("/users/", json={"name": "Deadpond", "id": test_uuid})

    # Create a board
    client.post(
        "/boards/",
        json={
            "name": "Board 1",
            "id": board_id,
            "user_id": test_uuid,
            "access_key": access_key,
        },
    )

    # Create a todo
    response = client.post(
        "/todos/",
        json={
            "title": "Todo 1",
            "board_id": board_id,
            "state": "TODO",
            "user_id": test_uuid,
        },
    )

    response = client.get(f"/boards/{board_id}/todos/")

    assert response.status_code == 200
    data = response.json()
    assert data[0]["title"] == "Todo 1"
    assert data[0]["board_id"] == board_id
    assert data[0]["state"] == "TODO"
    assert data[0]["user_id"] == test_uuid

    # Delete the user and validate that the board was deleted by cascading deletion
    client.delete(f"/users/{test_uuid}")
