

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
