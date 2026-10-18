import os
import pytest
from app import create_app
from app.extensions import db as _db
from app.models.user import User
from app.services.auth_service import AuthService


@pytest.fixture(scope="session")
def app():
    os.environ["FLASK_ENV"] = "testing"
    app = create_app("testing")
    return app


@pytest.fixture(scope="function")
def client(app):
    with app.app_context():
        _db.create_all()
        yield app.test_client()
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def auth_headers_user1(client):
    res = client.post(
        "/api/v1/auth/register",
        json={"email": "alice@example.com", "password": "Password123!", "full_name": "Alice Smith"},
    )
    token = res.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_user2(client):
    res = client.post(
        "/api/v1/auth/register",
        json={"email": "bob@example.com", "password": "Password123!", "full_name": "Bob Jones"},
    )
    token = res.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
