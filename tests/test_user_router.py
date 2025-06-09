import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.user.model import User
from src.auth.auth import get_passwd_hash


@pytest.mark.asyncio
async def test_create_user(client: TestClient):
    response = client.post(
        "/auth/register", json={"username": "testuser", "email": "test@example.com", "password": "password123", "phone": "123-456-7890"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_list_users(client: TestClient, session: Session):
    # Create a user directly in the session for testing list
    user_1 = User(username="user1", email="user1@example.com", passwd_hash=get_passwd_hash("password1"), phone="111-222-3333")
    user_2 = User(username="user2", email="user2@example.com", passwd_hash=get_passwd_hash("password2"), phone="444-555-6666")
    session.add(user_1)
    await session.commit() # Await commit
    await session.refresh(user_1) # Await refresh
    session.add(user_2)
    await session.commit() # Await commit
    await session.refresh(user_2) # Await refresh

    response = client.get("/user/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["username"] == "user1"
    assert data[1]["username"] == "user2"


@pytest.mark.asyncio
async def test_get_user(client: TestClient, session: Session):
    user = User(username="singleuser", email="single@example.com", passwd_hash=get_passwd_hash("password"), phone="777-888-9999")
    session.add(user)
    await session.commit() # Await commit
    await session.refresh(user) # Await refresh

    response = client.get(f"/user/{user.id}")
    assert response.status_code == 200
    assert response.json()["username"] == "singleuser"

    response = client.get("/user/999")  # Non-existent user
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_update_user(client: TestClient, session: Session):
    user = User(username="oldname", email="old@example.com", passwd_hash=get_passwd_hash("oldpassword"), phone="000-111-2222")
    session.add(user)
    await session.commit() # Await commit
    await session.refresh(user) # Await refresh

    response = client.put(
        f"/user/{user.id}", json={"email": "new@example.com", "phone": "333-444-5555"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "new@example.com"

    response = client.put(
        "/user/999", json={"phone": "999-999-9999"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_delete_user(client: TestClient, session: Session):
    user = User(username="todelete", email="delete@example.com", passwd_hash=get_passwd_hash("password"), phone="666-777-8888")
    session.add(user)
    await session.commit() # Await commit
    await session.refresh(user) # Await refresh

    response = client.delete(f"/user/{user.id}")
    assert response.status_code == 200
    assert response.json()["username"] == "todelete"

    response = client.get(f"/user/{user.id}")
    assert response.status_code == 404

    response = client.delete("/user/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
