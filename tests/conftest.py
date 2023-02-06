import pytest
from starlette.testclient import TestClient

import elevatus_poc.main
from apps.candidates.constants import Gender
from elevatus_poc.core.database import database

base_url = "api/v1/"



@pytest.fixture(scope="session")
def test_user():
    return {
        "firstname": "test",
        "lastname": "test",
        "email": "test@nomail.com",
        "password": "password",
    }


@pytest.fixture(scope="session")
def test_user_for_auth_client():
    return {
        "firstname": "test1",
        "lastname": "test1",
        "email": "test1@nomail.com",
        "password": "password",
    }


@pytest.fixture(scope="session")
def test_candidate():
    return {
        "firstname": "John",
        "lastname": "smith",
        "email": "jon@usa.com",
        "career_level": "junior",
        "job_major": "Computer Science",
        "years_of_experience": 5,
        "degree_type": "Master",
        "skills": ["Python", "Mongodb"],
        "nationality": "test",
        "city": "test",
        "salary": "1000",
        "gender": Gender.MALE.value,
    }


@pytest.fixture(scope="session")
def test_client():
    application = elevatus_poc.main.app
    with TestClient(application) as test_client:
        yield test_client

    db = database


@pytest.fixture(scope="session")
def test_create_user_for_auth_client(test_client, test_user_for_auth_client):
    response = test_client.post(f"{base_url}user/", json=test_user_for_auth_client)
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="session")
def generate_access_token(test_client, test_create_user_for_auth_client):
    data = {
        "email": str(test_create_user_for_auth_client['email']),
        "password": "password"
    }
    response = test_client.post(f"{base_url}login", json=data)
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="session")
def authorized_client(generate_access_token):
    application = elevatus_poc.main.app
    with TestClient(application) as test_client:
        test_client.headers['Authorization'] = "Bearer " + str(generate_access_token['access'])
        yield test_client

    db = database


@pytest.fixture(scope="session")
def unauthorized_client(generate_access_token):
    application = elevatus_poc.main.app
    with TestClient(application) as test_client:
        yield test_client

    db = database