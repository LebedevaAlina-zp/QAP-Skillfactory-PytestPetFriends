import pytest
from api import PetFriends
from settings import valid_email, valid_password
import generate_str

pf = PetFriends()

@pytest.mark.list
@pytest.mark.positive
@pytest.mark.parametrize('filter', ['', 'my_pets'],
                         ids=['no filter', 'my_pets'])
@pytest.mark.parametrize("accept",
                         ["application/json", "application/xml", generate_str.n_string(30)],
                         ids = ["application/json", "application/xml", "30 chars string"])
def test_valid_filter(get_key, filter, accept):
    """Check the response status is 200 and the result contains a non-empty list of pets for get_pets_list request with
     valid filters"""

    status, result = pf.get_pets_list(get_key, filter, accept=accept)
    assert status == 200
    assert 'pets' in result
    assert len(result['pets']) > 0


@pytest.mark.list
@pytest.mark.positive
@pytest.mark.parametrize("accept",
                         ["application/json", "application/xml", generate_str.n_string(30)],
                         ids = ["application/json", "application/xml", "30 chars string"])
@pytest.mark.parametrize("content_type",
                         ["application/json", "text/html", generate_str.n_string(20)],
                         ids = ["application/json", "application/xml", "20 chars string"])
def test_valid_content_type_accept_headers(get_key, accept, content_type, filter='my_pets'):
    """Check the response status is 200 and the result contains a non-empty list of pets for get_pets_list request with
     different headers"""

    status, result = pf.get_pets_list(get_key, filter, accept=accept, content_type=content_type)
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
    """Check the response code is 400 for all unacceptable filter values sent for a pets list request."""

    status, result = pf.get_pets_list(get_key, filter)
    assert status == 400


@pytest.mark.list
@pytest.mark.negative
@pytest.mark.parametrize('auth_key',
                         [{'key': ''}, {'key': f'{generate_str.n_string(255)}'},
                          {'key': f'{generate_str.n_string(1000)}'}, {'key': '5'}],
                         ids=['empty str', '255 chars', '1000 chars', 'integer'])
def test_my_pets_wrong_key(auth_key, filter='my_pets'):
    """Check a user can't get a list of pets with a wrong auth_key."""

    status, result = pf.get_pets_list(auth_key, filter)

    assert status == 403
