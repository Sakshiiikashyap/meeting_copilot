def test_register_new_user(client):
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpass123", "full_name": "Test User"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data  # password should never be exposed


def test_register_duplicate_email_fails(client):
    client.post("/auth/register", json={"email": "dup@example.com", "password": "pass123"})
    response = client.post("/auth/register", json={"email": "dup@example.com", "password": "pass456"})
    assert response.status_code == 400


def test_login_with_correct_credentials(client):
    client.post("/auth/register", json={"email": "login@example.com", "password": "correctpass"})
    response = client.post("/auth/login", json={"email": "login@example.com", "password": "correctpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_with_wrong_password_fails(client):
    client.post("/auth/register", json={"email": "wrong@example.com", "password": "correctpass"})
    response = client.post("/auth/login", json={"email": "wrong@example.com", "password": "wrongpass"})
    assert response.status_code == 401


def test_me_requires_authentication(client):
    response = client.get("/auth/me")
    assert response.status_code in (401, 403)


def test_me_returns_current_user(client):
    client.post("/auth/register", json={"email": "me@example.com", "password": "pass123"})
    login_res = client.post("/auth/login", json={"email": "me@example.com", "password": "pass123"})
    token = login_res.json()["access_token"]

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"