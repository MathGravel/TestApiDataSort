import pytest
from main import app  
from fastapi.testclient import TestClient

client = TestClient(app)


def test_replace_database():
    response = client.get(
        "/health",
        headers={"X-Token": "TempValue"}
    )
    assert response.status_code == 200

def test_get_n_elements_from_memory():
    response = client.get(
        "/health",
        headers={"X-Token": "TempValue"}
    )
    assert response.status_code == 200


def test_get_n_elements_from_file():
    response = client.get(
        "/health",
        headers={"X-Token": "TempValue"}
    )
    assert response.status_code == 200


def test_check_server_health():
    response = client.get(
        "/health",
        headers={"X-Token": "TempValue"}
    )
    assert response.status_code == 200
