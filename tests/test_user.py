import pytest

from tests.conftest import base_url


def test_add_user(test_client, test_user):
    response = test_client.post(f"{base_url}user/", json=test_user)
    assert response.status_code == 200
    assert response.json()["firstname"] == "test"
    assert response.json()["lastname"] == "test"
    assert response.json()["email"] == "test@nomail.com"


def test_add_user_with_same_email(test_client, test_user):
    response = test_client.post(f"{base_url}user/", json=test_user)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Email already exist"
    }


def test_add_user_with_incorrect_data(test_client):
    data = {
        "firstname": "Jack",
        "lastname": "jill",
        "email": "jack",
        "password": "test"
    }
    response = test_client.post(f"{base_url}user/", json=data)
    assert response.status_code == 422


def test_login(test_client):
    data = {
        "email": "test@nomail.com",
        "password": "password"
    }
    response = test_client.post(f"{base_url}login", json=data)
    assert response.status_code == 200


def test_login_with_incorrect_email(test_client):
    data = {
        "email": "tes@nomail.com",
        "password": "password"
    }
    response = test_client.post(f"{base_url}login", json=data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid email or password"
    }


