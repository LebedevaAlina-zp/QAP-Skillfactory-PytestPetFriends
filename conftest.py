import pytest
from settings import valid_email, valid_password
from api import PetFriends
from datetime import datetime

pf = PetFriends()

@pytest.fixture(scope="module")
def get_key():
    status_code, auth_key = pf.get_api_key(valid_email, valid_password)
    assert status_code == 200, 'Key request failed'
    assert 'key' in auth_key, 'No key in the response for the key request'
    return auth_key

@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print(f"\nThe test lasted: {end_time - start_time}")


