import pytest
from api import PetFriends
from settings import valid_email, valid_password
import generate_str

pf = PetFriends()

@pytest.mark.add_simple
@pytest.mark.positive
@pytest.mark.parametrize('name',
                         ['Kitty', generate_str.russian_chars(), generate_str.n_string(255)],
                         ids=['latin name', 'russian name', '255 chars name'])
@pytest.mark.parametrize('animal_type',
                         ['Kitten', generate_str.russian_chars(), generate_str.n_string(255)],
                         ids=['latin animal type', 'russian animal type', '255 chars animal type'])
@pytest.mark.parametrize('age',
                         ['10', '  4  ', '0'],
                         ids=['integer age', 'int with spaces age', '0 age'])
def test_valid_data(get_key, name, animal_type, age):
    """Check a user can add a pet without a photo correctly with differrent valid names, animal types and ages."""

    # Add a new pet without a photo
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name \
           and result['animal_type'] == animal_type \
           and result['age'] == age


@pytest.mark.add_simple
@pytest.mark.negative
@pytest.mark.parametrize('auth_key',
                         [{'key': ''}, {'key': f'{generate_str.n_string(255)}'},
                          {'key': f'{generate_str.n_string(1000)}'}, {'key': '5'}],
                         ids=['empty str', '255 chars', '1000 chars', 'integer'])
def test_wrong_key(auth_key, name="Kitty", animal_type="Kitten", age="0"):
    """Check a user can't add a pet with incorrect values for auth_key."""

    # Add a new pet without a photo
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 403


@pytest.mark.skip(reason="This tests fail because the application doesn't apply any conditions to pet's name now.")
@pytest.mark.add_simple
@pytest.mark.negative
@pytest.mark.parametrize('name',
                         ['', generate_str.n_string(1000), generate_str.chinese_chars(), generate_str.special_chars()],
                         ids=['empty str', '1000 chars', 'chinese chars', 'special chars'])
def test_invalid_name(get_key, name, animal_type="Kitten", age="0"):
    """Check a user can't add a pet with incorrect values for pet's name, and get a server rensponse 400 but not 500."""

    # Add a new pet without a photo
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    assert status == 400


@pytest.mark.skip(reason="This tests fail because the application doesn't apply any conditions to pet's animal type now.")
@pytest.mark.add_simple
@pytest.mark.negative
@pytest.mark.parametrize('animal_type',
                         ['', generate_str.n_string(1000), generate_str.chinese_chars(), generate_str.special_chars()],
                         ids=['empty str', '1000 chars', 'chinese chars', 'special chars'])
def test_invalid_name(get_key, animal_type, name='Whitney', age="0"):
    """Check a user can't add a pet with incorrect values for animal type, and get a server rensponse 400 but not 500."""

    # Add a new pet without a photo
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    assert status == 400


@pytest.mark.skip(reason="This tests fail because the application doesn't apply any conditions to pet's age and treat "
                         "this input parameter as a usual string.")
@pytest.mark.add_simple
@pytest.mark.negative
@pytest.mark.parametrize('age',
                         ['', '-12', '4.3', '4,5', generate_str.n_string(255), generate_str.n_string(1000),
                          generate_str.chinese_chars(), generate_str.special_chars()],
                         ids=['empty str', 'negative number', 'noninteger with a dot', 'noninteger with a coma',
                              '255 chars', '1000 chars', 'chinese chars', 'special chars'])
def test_invalid_age(get_key, age, name="Kitty", animal_type="Kitten"):
    """Check a user can't add a pet with incorrect values for pet's age, and get a server rensponse 400 but not 500."""

    # Add a new pet without a photo
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    assert status == 400

