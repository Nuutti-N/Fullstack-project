

def test_welcome(client):
    response = client.get("/welcome")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the AI Agent"
    }


def test_chat_request_token(client):
    response = client.post("/chat")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_analyze_request_token(client):
    response = client.post("/analyze")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_history_request_token(client):
    response = client.get("/history")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_delete_history_request_token(client):
    response = client.delete("/delete_history/{fact_id}")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
