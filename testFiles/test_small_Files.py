from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_replace_database():
    with open('./testFiles/data/0-1k/test_n20_date_20241217104400.txt',
              'rb') as f:
        response = client.post("/replaceDataset",
                               files={"file": ("DB.txt", f, "text/plain")})
        assert response.status_code == 200


def test_get_n_elements_from_memory():

    with open('./testFiles/data/0-1k/test_n20_date_20241217104400.txt',
              'rb') as f:
        response = client.post("/replaceDataset",
                               files={"file": ("DB.txt", f, "text/plain")})
    assert response.status_code == 200
    response = client.get("/getValues/6", headers={"X-Token": "TempValue"})
    assert response.status_code == 200
    assert response.json() == {
        'values':
        [826188064, 583339512, 686239854, 631429245, 598046285, 639284544]
    }


def test_get_n_elements_from_file():
    with open('./testFiles/data/0-1k/test_n20_date_20241217104400.txt',
              'rb') as f:
        response = client.post("/uploadAndTreatFile/6",
                               files={"file": ("DB.txt", f, "text/plain")})
    assert response.status_code == 200
    assert response.json() == {
        'values':
        [360413580, 25234429, 851575837, 935905565, 792584932, 161395212]
    }


def test_send_wrong_format_file():
    with open('./testFiles/wrongInput.png',
              'rb') as f:
        response = client.post("/uploadAndTreatFile/6",
                               files={"file": ("DB.jpeg", f, "image/png")})
    assert response.status_code == 400


def test_check_server_health():
    response = client.get("/health", headers={"X-Token": "TempValue"})
    assert response.status_code == 200
