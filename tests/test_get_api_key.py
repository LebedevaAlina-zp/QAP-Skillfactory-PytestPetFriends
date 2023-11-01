import pytest
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

@pytest.mark.key
@pytest.mark.positive
def test_valid_user(email=valid_email, password=valid_password):
    """Check a valid user can get an auth_key using get_api_key method, make sure status code is 200 and the response
    contains 'key' """

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

@pytest.mark.key
@pytest.mark.negative
def test_wrong_password(email=valid_email, password=valid_password+"0"):
    """Check a user can't get an auth_key using get_api_key method with a wrong password"""

    #Make a request and save a resposponse status
    status, _ = pf.get_api_key(email, password)

    #Check the response status code is 403
    assert status == 403

@pytest.mark.key
@pytest.mark.positive
def test_uppercase_email(email=valid_email.upper(), password=valid_password):
    """Check a user still gets an auth_key, providing a valid but written uppercase name and a valid password"""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result

@pytest.mark.key
@pytest.mark.negative
def test_uppercase_password(email=valid_email, password=valid_password.upper()):
    """Check a user can't get an auth_key, roviding a valid name and a valid but by mistake written uppercase password"""

    status, _ = pf.get_api_key(email, password)

    assert status == 403