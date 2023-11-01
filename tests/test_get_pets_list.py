import pytest
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

@pytest.mark.list
@pytest.mark.positive
def test_all_pets_valid_key(get_key, filter=''):
    """Check the response status is 200 and the result contains a non-empty list of pets when a request via
    get_pets_list method with empty filter is made"""

    status, result = pf.get_pets_list(get_key, filter)
    assert status == 200
    assert 'pets' in result
    assert len(result['pets']) > 0

@pytest.mark.list
@pytest.mark.positive
def test_my_pets(get_key, filter="my_pets"):
    """Check that for a request for pets list with 'my_pets' filter the response has got non-empty list of pets.
     Проверяем что запрос питомцев с фильтром "my_pets" возвращает непустой список питомцев."""

    status, result = pf.get_pets_list(get_key, "my_pets")

    assert status == 200
    assert len(result['pets']) > 0

@pytest.mark.list
@pytest.mark.negative
def test_all_pets_wrong_key(get_key, filter=''):
    """Check a user can't get a list of pets with a wrong auth_key."""

    # Delete the last symbol in the key obtained
    wrong_key = get_key.copy()
    wrong_key['key'] = wrong_key['key'][:-1]

    status, result = pf.get_pets_list(wrong_key, filter)

    assert status == 403
