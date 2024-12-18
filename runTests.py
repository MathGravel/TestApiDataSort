import pytest
from main import generate  # Assuming the function to test is in main.py

@pytest.fixture
def setup_rng():
    import random
    rng = random.Random()
    yield rng

def test_generate_function(setup_rng):
    nInstances = 10
    rng = setup_rng
    result = generate(nInstances)
    
    assert isinstance(result, dict)
    assert "message" in result
    assert f"Generated {nInstances} instances" in result["message"]

def test_generate_file_content(setup_rng):
    nInstances = 5
    rng = setup_rng
    test_name = f"test_n{nInstances}_date_{{}}.txt".format(datetime.now().strftime("%Y%m%d%H%M%S"))
    
    # Call the function to generate the test file
    generate_test_file(nInstances, rng)
    
    with open(test_name, 'r') as f:
        lines = f.readlines()
    
    assert len(lines) == nInstances
    for line in lines:
        parts = line.strip().split('_')
        assert len(parts) == 2  # Each line should have two parts
        assert parts[0].isdigit()  # First part should be a number
        assert parts[1].isdigit()  # Second part should be a number


if __name__ == "__main__":
    pytest.main()