import pytest
from api import PetFriends
from settings import valid_email, valid_password
import generate_str

pf = PetFriends()

@pytest.mark.list
@pytest.mark.positive
@pytest.mark.parametrize('filter', ['', 'my_pets'],
                         ids=['no filter', 'my_pets'])
def test_valid_filter(get_key, filter):
    """Check the response status is 200 and the result contains a non-empty list of pets when a request via
    get_pets_list method with empty filter is made"""

    status, result = pf.get_pets_list(get_key, filter)
    assert status == 200
    assert 'pets' in result
    assert len(result['pets']) > 0


@pytest.mark.list
@pytest.mark.negative
@pytest.mark.parametrize('filter',
                         [generate_str.n_string(255), generate_str.n_string(1000), generate_str.russian_chars(),
                          generate_str.chinese_chars(), generate_str.special_chars()],
                         ids=['255 chars', '1000 chars', 'russian chars', 'chinese chars', 'special chars'])
def test_unacceptable_filter(get_key, filter):
    """Check the response code is 400 for all unacceptable filter values sent with a request for pets list."""
    status, result = pf.get_pets_list(get_key, filter)
    assert status == 400

@pytest.mark.list
@pytest.mark.negative
@pytest.mark.parametrize('auth_key',
                         [{'key': ''}, {'key': f'{generate_str.n_string(255)}'},
                          {'key': f'{generate_str.n_string(1000)}'}, {'key': f'{generate_str.russian_chars()}'},
                          {'key': f'{generate_str.chinese_chars()}'}, {'key': f'{generate_str.special_chars()}'},
                          {'key': 5}],
                         ids=['empty str', '255 chars', '1000 chars', 'russian chars', 'chinese chars', 'special chars',
                              'integer'])
def test_my_pets_wrong_key(auth_key, filter='my_pets'):
    """Check a user can't get a list of pets with a wrong auth_key."""

    status, result = pf.get_pets_list(auth_key, filter)

    assert status == 403
