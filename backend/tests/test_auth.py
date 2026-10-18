def test_register_and_login_success(client):
    # Register
    reg_res = client.post(
        "/api/v1/auth/register",
        json={"email": "newuser@example.com", "password": "SecurePassword1!", "full_name": "Test User"},
    )
    assert reg_res.status_code == 201
    reg_data = reg_res.get_json()
    assert reg_data["success"] is True
    assert "access_token" in reg_data["data"]
    assert reg_data["data"]["user"]["email"] == "newuser@example.com"

    # Login
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "newuser@example.com", "password": "SecurePassword1!"},
    )
    assert login_res.status_code == 200
    login_data = login_res.get_json()
    assert login_data["success"] is True
    assert "access_token" in login_data["data"]


def test_register_duplicate_email(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "Password123!"},
    )
    res = client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "Password123!"},
    )
    assert res.status_code == 409
    data = res.get_json()
    assert data["success"] is False
    assert data["error"]["code"] == "CONFLICT"


def test_register_weak_password(client):
    res = client.post(
        "/api/v1/auth/register",
        json={"email": "weak@example.com", "password": "short"},
    )
    assert res.status_code == 422
    data = res.get_json()
    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_login_invalid_password(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "valid@example.com", "password": "Password123!"},
    )
    res = client.post(
        "/api/v1/auth/login",
        json={"email": "valid@example.com", "password": "WrongPassword!"},
    )
    assert res.status_code == 401
    data = res.get_json()
    assert data["success"] is False
    assert data["error"]["code"] == "UNAUTHORIZED"


def test_logout_revokes_token(client):
    reg_res = client.post(
        "/api/v1/auth/register",
        json={"email": "logout@example.com", "password": "Password123!"},
    )
    token = reg_res.get_json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Verify access before logout
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200

    # Logout
    logout_res = client.post("/api/v1/auth/logout", headers=headers)
    assert logout_res.status_code == 200

    # Verify access is revoked
    revoked_res = client.get("/api/v1/auth/me", headers=headers)
    assert revoked_res.status_code == 401
