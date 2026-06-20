from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200


#def test_register():
#    response = client.post(
#        "register",
#        json={
#            "email": "test@test1.com",
#            "username": "testuser",
#            "password": "password123"
#        }
#    )
#    assert response.status_code == 200


def test_login():
    response = client.post(
        "/login",
        json={
            "email": "test@test1.com",
            "password": "password123"
        }
    )
    assert response.status_code==200