from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users", json={
        "name": "Ashwin",
        "email": "ashwin@example.com"
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data or "_id" in data

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
