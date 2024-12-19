import pytest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_replace_database():
    with open('./testFiles/data/10k-100k/test_n100000_date_20241218120240.txt',
              'rb') as f:
        response = client.post("/replaceDataset",
                               files={"file": ("DB.txt", f, "text/plain")})
        assert response.status_code == 200


def test_get_n_elements_from_memory():

    with open('./testFiles/data/10k-100k/test_n100000_date_20241218120240.txt',
              'rb') as f:
        response = client.post("/replaceDataset",
                               files={"file": ("DB.txt", f, "text/plain")})
    assert response.status_code == 200
    response = client.get("/getValues/6", headers={"X-Token": "TempValue"})

    assert response.status_code == 200
    assert response.json() == {
        'values':
        [396922357, 463486948, 269971815, 308497780, 787919671, 1014815318]
    }


def test_get_n_elements_from_file():
    with open('./testFiles/data/10k-100k/test_n100000_date_20241218183031.txt',
              'rb') as f:
        response = client.post("/uploadAndTreatFile/6",
                               files={"file": ("DB.txt", f, "text/plain")})

    assert response.status_code == 200
    assert response.json() == {
        'values': [
            774653051622209, 495927890500101, 1094354938371475,
            520197759693291, 351266651470455, 1064532899411157
        ]
    }


def test_check_server_health():
    response = client.get("/health", headers={"X-Token": "TempValue"})
    assert response.status_code == 200
