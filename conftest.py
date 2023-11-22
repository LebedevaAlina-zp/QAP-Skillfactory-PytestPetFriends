import pytest
from settings import valid_email, valid_password
from settings import other_email, other_password
from api import PetFriends
from datetime import datetime

pf = PetFriends()

@pytest.fixture(scope='module')
def get_key():
    """ Get an auth key fixture allows to get a key only once before all the tests and use it in each test. """
    status_code, auth_key = pf.get_api_key(valid_email, valid_password)
    assert status_code == 200, 'Key request failed'
    assert 'key' in auth_key, 'No key in the response for the key request'
    return auth_key


@pytest.fixture(scope='module')
def pet_with_image(get_key):
    """ Get a pet fixture create's and returns a pet with an image"""

    _, pet = pf.add_new_pet(get_key, 'Alice', 'Cat', '3', 'images/jpg_pic.jpg')

    return pet


@pytest.fixture(scope="module")
def other_key():
    """ Get an auth key fixture allows to get a key only once before all the tests and use it in each test. """
    status_code, auth_key = pf.get_api_key(other_email, other_password)
    assert status_code == 200, 'Key request failed'
    assert 'key' in auth_key, 'No key in the response for the key request'
    return auth_key


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print(f"\nThe test lasted: {end_time - start_time}")


