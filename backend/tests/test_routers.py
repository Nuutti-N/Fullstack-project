
def test_welcome(client):
    response = client.get("/welcome")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the AI Agent"
    }
