import pytest
from api import PetFriends
from settings import valid_email, valid_password
import generate_str

pf = PetFriends()

@pytest.mark.key
@pytest.mark.positive
@pytest.mark.parametrize("email",
                         [valid_email, valid_email.upper(), valid_email + '   '],
                         ids = ['valid email', 'capslock email', 'spaces after email'])
@pytest.mark.parametrize("password",
                         [valid_password, valid_password + '   '],
                         ids = ['valid password', 'spaces after password'])
def test_valid_user(email, password):
    """Check a valid user can get an auth_key using get_api_key method, make sure status code is 200 and the response
    contains 'key' """

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


@pytest.mark.key
@pytest.mark.negative
@pytest.mark.parametrize('email',
                         ['', generate_str.n_string(255), generate_str.n_string(1000),
                          #generate_str.special_chars(), generate_str.russian_chars(), generate_str.chinese_chars(),
                          # Not allowed for hhtp requests to have not ASCII symbols in headers
                          '59'],
                         ids=['empty string', '255 chars', '1000 chars',
                              #'special chars', 'russian chars', 'chinese chars',
                              'integer'])
def test_wrong_email(email, password=valid_password):
    """Check a user can't get an auth_key using get_api_key method with a wrong email"""

    #Make a request and save a resposponse status
    status, _ = pf.get_api_key(email, password)

    #Check the response status code is 403
    assert status == 403



@pytest.mark.key
@pytest.mark.negative
@pytest.mark.parametrize('password',
                         ['', generate_str.n_string(255), generate_str.n_string(1000), valid_password.upper(),
                          #generate_str.special_chars(), generate_str.russian_chars(), generate_str.chinese_chars(),
                          # Not allowed for hhtp requests to have not ASCII symbols in headers
                          '59'],
                         ids=['empty string', '255 chars', '1000 chars', 'password capslock',
                              #'special chars', 'russian chars', 'chinese chars',
                              'integer'])
def test_wrong_password(password, email=valid_email):
    """Check a user can't get an auth_key using get_api_key method with a wrong password"""

    #Make a request and save a resposponse status
    status, _ = pf.get_api_key(email, password)

    #Check the response status code is 403
    assert status == 403
