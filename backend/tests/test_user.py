

from tokenize import Token


def test_signup(client):
    response = client.post(
        "/signup", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    #  If another person try to signup same username, so then give Username exists
    response = client.post(
        "/signup", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Username exists"


def test_login(client):
    response = client.post(
        "/login", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_login_fail(client):
    response = client.post(
        "/login", data={"username": "us", "password": "time12"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect Username or password"


def test_your_requires_token(client):
    response = client.get("/your")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_works_with_token(client):
    # sign up first
    response = client.post(
        "/signup", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 400
    # then login
    login = client.post(
        "/login", data={"username": "testuser", "password": "testpass"})
    assert login.status_code == 200
    token = login.json()["access_token"]
    response = client.get(
        "/your", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert isinstance(token, str) and token
    assert "id" in data
