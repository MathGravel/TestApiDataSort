import pytest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_replace_database():
    with open(
            './testFiles/data/100k-1000k/test_n1000000_date_20241218120251.txt',
            'rb') as f:
        response = client.post("/replaceDataset",
                               files={"file": ("DB.txt", f, "text/plain")})
        assert response.status_code == 200


def test_get_n_elements_from_memory():

    with open(
            './testFiles/data/100k-1000k/test_n1000000_date_20241218120251.txt',
            'rb') as f:
        response = client.post("/replaceDataset",
                               files={"file": ("DB.txt", f, "text/plain")})
    assert response.status_code == 200
    response = client.get("/getValues/6", headers={"X-Token": "TempValue"})
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        'values': [
            463166267, 151894931, 392836611, 269735467, 904922347, 83063453
        ]
    }


def test_get_n_elements_from_file():
    with open(
            './testFiles/data/100k-1000k/test_n1000000_date_20241218182854.txt',
            'rb') as f:
        response = client.post("/uploadAndTreatFile/6",
                               files={"file": ("DB.txt", f, "text/plain")})
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        'values': [
            765051075082450, 915421971660748, 11422033216229, 751747014997266,
            589763783115283, 534755891735904
        ]
    }


def test_check_server_health():
    response = client.get("/health", headers={"X-Token": "TempValue"})
    assert response.status_code == 200
