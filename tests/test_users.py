from fastapi.testclient import TestClient
from tests.test_database import client, session

# client = TestClient(app)

def test_home(client):
    response = client.get('/')
    print(response.json())
    assert response.status_code == 200


def test_create_user(client):
    res = client.post('/user/signup/', json={"username":"mic", "email":"mic@gmail.com", "password":"password"})
    print(res.json())
    assert res.status_code == 201


def test_login_user(client):
    res = client.post('/login/', data={"username":"mic@gmail.com", "password":"password"})
    print(res.json())
    assert res.status_code == 200