from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_replace_database():
    with open('./testFiles/data/1k-10k/test_n10000_date_20241218120213.txt',
              'rb') as f:
        response = client.post("/replaceDataset",
                               files={"file": ("DB.txt", f, "text/plain")})
        assert response.status_code == 200


def test_get_n_elements_from_memory():

    with open('./testFiles/data/1k-10k/test_n10000_date_20241218120213.txt',
              'rb') as f:
        response = client.post("/replaceDataset",
                               files={"file": ("DB.txt", f, "text/plain")})
    assert response.status_code == 200
    response = client.get("/getValues/6", headers={"X-Token": "TempValue"})
    assert response.status_code == 200
    assert response.json() == {
        'values':
        [878187727, 593261804, 502862459, 971170979, 491453651, 143858901]
    }


def test_get_n_elements_from_file():
    with open('./testFiles/data/1k-10k/test_n10000_date_20241218183048.txt',
              'rb') as f:
        response = client.post("/uploadAndTreatFile/6",
                               files={"file": ("DB.txt", f, "text/plain")})
    assert response.status_code == 200
    assert response.json() == {
        'values': [
            759206813774819, 415504084825442, 635496524931843, 247052238260448,
            744800770637176, 46872948794798
        ]
    }
