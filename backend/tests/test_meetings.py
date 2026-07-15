def test_create_meeting(client, auth_headers):
    response = client.post(
        "/meetings/",
        json={"title": "Test Meeting", "raw_transcript": "This is a test transcript."},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Meeting"
    assert data["status"] == "uploaded"


def test_create_meeting_requires_auth(client):
    response = client.post(
        "/meetings/",
        json={"title": "Test", "raw_transcript": "Text"},
    )
    assert response.status_code in (401, 403)


def test_list_meetings_returns_only_own_meetings(client):
    # user A creates a meeting
    client.post("/auth/register", json={"email": "userA@example.com", "password": "pass123"})
    login_a = client.post("/auth/login", json={"email": "userA@example.com", "password": "pass123"})
    headers_a = {"Authorization": f"Bearer {login_a.json()['access_token']}"}
    client.post("/meetings/", json={"title": "A's Meeting", "raw_transcript": "text"}, headers=headers_a)

    # user B creates a different meeting
    client.post("/auth/register", json={"email": "userB@example.com", "password": "pass123"})
    login_b = client.post("/auth/login", json={"email": "userB@example.com", "password": "pass123"})
    headers_b = {"Authorization": f"Bearer {login_b.json()['access_token']}"}
    client.post("/meetings/", json={"title": "B's Meeting", "raw_transcript": "text"}, headers=headers_b)

    # user A should only see their own meeting
    response = client.get("/meetings/", headers=headers_a)
    titles = [m["title"] for m in response.json()]
    assert "A's Meeting" in titles
    assert "B's Meeting" not in titles


def test_cannot_access_other_users_meeting(client):
    client.post("/auth/register", json={"email": "owner@example.com", "password": "pass123"})
    login_owner = client.post("/auth/login", json={"email": "owner@example.com", "password": "pass123"})
    headers_owner = {"Authorization": f"Bearer {login_owner.json()['access_token']}"}
    create_res = client.post(
        "/meetings/", json={"title": "Private Meeting", "raw_transcript": "secret"}, headers=headers_owner
    )
    meeting_id = create_res.json()["id"]

    client.post("/auth/register", json={"email": "intruder@example.com", "password": "pass123"})
    login_intruder = client.post("/auth/login", json={"email": "intruder@example.com", "password": "pass123"})
    headers_intruder = {"Authorization": f"Bearer {login_intruder.json()['access_token']}"}

    response = client.get(f"/meetings/{meeting_id}", headers=headers_intruder)
    assert response.status_code == 403


def test_delete_meeting(client, auth_headers):
    create_res = client.post(
        "/meetings/", json={"title": "To Delete", "raw_transcript": "text"}, headers=auth_headers
    )
    meeting_id = create_res.json()["id"]

    delete_res = client.delete(f"/meetings/{meeting_id}", headers=auth_headers)
    assert delete_res.status_code == 204

    get_res = client.get(f"/meetings/{meeting_id}", headers=auth_headers)
    assert get_res.status_code == 404


def test_update_meeting_title_preserves_other_fields(client, auth_headers):
    create_res = client.post(
        "/meetings/", json={"title": "Original", "raw_transcript": "text"}, headers=auth_headers
    )
    meeting_id = create_res.json()["id"]

    update_res = client.put(
        f"/meetings/{meeting_id}", json={"title": "Updated"}, headers=auth_headers
    )
    assert update_res.status_code == 200
    assert update_res.json()["title"] == "Updated"
    assert update_res.json()["raw_transcript"] == "text"  # untouched