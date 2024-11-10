import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from main import app, get_session


@pytest.fixture(scope="module")
def test_client():
    engine = create_engine(
        "postgresql://postgres:postgrespassword@localhost:5433/postgres"
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


def test_create_hero(test_client):
    client = test_client

    response = client.post(
        "/heroes/", json={"name": "Deadpond", "secret_name": "Dive Wilson"}
    )

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpond"
    assert data["secret_name"] == "Dive Wilson"
    assert data["age"] is None
    assert data["id"] is not None
