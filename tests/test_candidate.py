import pytest

from apps.candidates.constants import Gender
from tests.conftest import base_url


def test_add_candidate(authorized_client, test_candidate):
    response = authorized_client.post(f"{base_url}candidate/", json=test_candidate)
    assert response.status_code == 200
    assert response.json()["firstname"] == "John"
    assert response.json()["lastname"] == "smith"
    assert response.json()["email"] == "jon@usa.com"


def test_add_candidate_with_unauthorized_client(unauthorized_client, test_candidate):
    response = unauthorized_client.post(f"{base_url}candidate/", json=test_candidate)
    assert response.status_code == 401


def test_add_candidate_with_different_url(authorized_client, test_candidate):
    response = authorized_client.post(f"{base_url}/candidate/", json=test_candidate)
    assert response.status_code == 404


def test_add_candidate_with_same_email(authorized_client, test_candidate):
    response = authorized_client.post(f"{base_url}candidate/", json=test_candidate)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Email already exist"
    }


@pytest.fixture()
def create_candidate(authorized_client, test_candidate):
    data = {
        "firstname": "John",
        "lastname": "smith",
        "email": "jack@nomail.com",
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
    response = authorized_client.post(f"{base_url}candidate/", json=data)
    assert response.status_code == 200
    return response.json()


def test_get_candidate_by_id(authorized_client, create_candidate):
    candidate_id = str(create_candidate['_id'])
    response = authorized_client.get(f"{base_url}candidate/{candidate_id}")
    assert response.status_code == 200
    assert response.json()["firstname"] == "John"
    assert response.json()["lastname"] == "smith"
    assert response.json()["email"] == "jack@nomail.com"


def test_get_candidate_by_different_id(authorized_client):
    candidate_id = "63e0b97c5b93e112a1035b76"
    response = authorized_client.get(f"{base_url}candidate/{candidate_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Candidate not found"
    }


@pytest.fixture()
def create_candidate_for_updating(authorized_client):
    data = {
        "firstname": "Jack",
        "lastname": "smith",
        "email": "jack@no.com",
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
    response = authorized_client.post(f"{base_url}candidate/", json=data)
    assert response.status_code == 200
    return response.json()


def test_update_candidate(authorized_client, create_candidate_for_updating):
    candidate_id = str(create_candidate_for_updating['_id'])
    data = {
        "firstname": "John",
        "lastname": "smith",
        "career_level": "junior",
        "job_major": "Computer Science",
        "years_of_experience": 5,
        "degree_type": "Master",
        "skills": ["Python", "Mongodb"],
        "nationality": "test",
        "city": "test",
        "salary": "100000",
        "gender": Gender.FEMALE.value,
    }
    response = authorized_client.put(f"{base_url}candidate/{candidate_id}", json=data)
    assert response.status_code == 200


@pytest.fixture()
def create_candidate_for_deleting(authorized_client):
    data = {
        "firstname": "Jack",
        "lastname": "smith",
        "email": "sparrow@no.com",
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
    response = authorized_client.post(f"{base_url}candidate/", json=data)
    assert response.status_code == 200
    return response.json()


def test_deleted_candidate(authorized_client, create_candidate_for_deleting):
    candidate_id = str(create_candidate_for_deleting['_id'])
    response = authorized_client.delete(f"{base_url}candidate/{candidate_id}")
    assert response.status_code == 200
    assert response.json() == "Candidate deleted success"


def test_delete_candidate_with_different_id(authorized_client):
    candidate_id = "63e0f1cd392393c37aa90c43"
    response = authorized_client.delete(f"{base_url}candidate/{candidate_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Candidate not found"
    }


def test_get_all_candidates(authorized_client):
    response = authorized_client.get(f"{base_url}candidate/all")
    assert response.status_code == 200


def test_get_all_candidate_with_unauthorized_client(unauthorized_client):
    response = unauthorized_client.get(f"{base_url}candidate/all")
    assert response.status_code == 401


def test_get_generated_report(authorized_client):
    response = authorized_client.get(f"{base_url}candidate/generate-report")
    assert response.status_code == 200


def test_get_generated_report_with_unauthorized_client(unauthorized_client):
    response = unauthorized_client.get(f"{base_url}candidate/generate-report")
    assert response.status_code == 401
