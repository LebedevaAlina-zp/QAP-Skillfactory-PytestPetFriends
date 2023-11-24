import pytest
from api import PetFriends
from settings import valid_email, valid_password
import os
import generate_str

pf = PetFriends()


@pytest.mark.update
@pytest.mark.positive
@pytest.mark.parametrize('name',
                         ['Carrie', 'Мурзик', '猫猫',
                                  generate_str.n_string(255), '1900', '', generate_str.special_chars()],
                         ids=['English name', 'Russian name', 'Chinese name',
                              '255 chars name', 'number name', 'empty name', 'special chars name'])
def test_valid_name(get_key, pet_with_image, name, animal_type='Mao', age='5'):
    """Check a user can update one's pet's name correctly."""

    # Remember pet_photo to make sure it won't change after pet's info update
    pet_photo = pet_with_image['pet_photo']

    # Try to update the pet's info
    status, result = pf.update_pet_info(get_key, pet_with_image['id'], name, animal_type, age)

    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age \
           and result['pet_photo'] == pet_photo


@pytest.mark.update
@pytest.mark.positive
@pytest.mark.parametrize('animal_type',
                         ['siamese cat', 'сиамская кошка', '暹罗猫',
                          generate_str.n_string(255), '123', '', generate_str.special_chars()],
                         ids=['english animal type', 'russian animal type', 'chinese animal type',
                              '255 chars animal type', 'number animal type', 'empty animal type',
                              'special chars animal type'])
def test_valid_animal_type(get_key, pet_with_image, animal_type, name='Meimei', age='5'):
    """Check a user can update one's pet's animal type correctly."""

    # Remember pet_photo to make sure it won't change after pet's info update
    pet_photo = pet_with_image['pet_photo']

    # Try to update the pet's info
    status, result = pf.update_pet_info(get_key, pet_with_image['id'], name, animal_type, age)

    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age \
           and result['pet_photo'] == pet_photo


@pytest.mark.update
@pytest.mark.positive
@pytest.mark.parametrize('age',
                         ['2', ' 3 ', '0', '', '3.5', '5.2',],
                         ids=['int age', 'int age with spaces', '0 age',
                              'empty age','noninteger age with a dot', 'noninteger age with a coma'])
def test_valid_age(get_key, pet_with_image, age, name='Meimei', animal_type='siamese cat'):
    """Check a user can update one's pet's age correctly."""

    # Remember pet_photo to make sure it won't change after pet's info update
    pet_photo = pet_with_image['pet_photo']

    # Try to update the pet's info
    status, result = pf.update_pet_info(get_key, pet_with_image['id'], name, animal_type, age)

    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age \
           and result['pet_photo'] == pet_photo


@pytest.mark.update
@pytest.mark.negaive
@pytest.mark.parametrize('auth_key',
                         [{'key': ''}, {'key': f'{generate_str.n_string(255)}'},
                          {'key': f'{generate_str.n_string(1000)}'}],
                         ids=['empty str', '255 chars', '1000 chars'])
def test_wrong_key(pet_with_image, auth_key, name='Carrie', animal_type='siamese cat', age='8'):
    """Check a user can't update pet's info with a wrong auth_key and have a response 403 statuc code."""

    # Remember pet_photo to make sure it won't change after pet's info update
    pet_photo = pet_with_image['pet_photo']

    # Try to update the pet's info
    status, result = pf.update_pet_info(auth_key, pet_with_image['id'], name, animal_type, age)

    assert status == 403


@pytest.mark.update
@pytest.mark.negaive
@pytest.mark.parametrize('pet_id',
                         ['', generate_str.n_string(255), generate_str.n_string(1000)],
                         ids=['empty string', '255 chars', '1000 chars'])
def test_wrong_id(get_key, pet_id, name='Carrie', animal_type='siamese cat', age='8'):
    """ Check a user can't update pet's info with a wrong pet_id and gets 404 or 400 response status. """

    # Try to update the pet's info
    status, result = pf.update_pet_info(get_key, pet_id, name, animal_type, age)

    assert status == 404 or 400


@pytest.mark.skip(reason="This tests fail because the application doesn't apply any conditions to pet's name")
@pytest.mark.update
@pytest.mark.negative
@pytest.mark.parametrize('name',
                         [generate_str.n_string(1000)],
                         ids=['1000 chars'])
def test_invalid_name(get_key, pet_with_image, name, animal_type='siamese cat', age='4'):
    """Check a user can't update one's pet's name with invalid value. """

    # Try to update the pet's info
    status, result = pf.update_pet_info(get_key, pet_with_image['id'], name, animal_type, age)

    assert status == 400


@pytest.mark.skip(reason="This tests fail because the application doesn't apply any conditions to pet's animal type")
@pytest.mark.update
@pytest.mark.negative
@pytest.mark.parametrize('animal_type',
                         [generate_str.n_string(1000)],
                         ids=['1000 chars'])
def test_invalid_animal_type(get_key, pet_with_image, animal_type, name='Kitty', age='4'):
    """Check a user can't update one's pet's animal_type with invalid value. """

    # Try to update the pet's info
    status, result = pf.update_pet_info(get_key, pet_with_image['id'], name, animal_type, age)

    assert status == 400


@pytest.mark.skip(reason="This tests fail because the application doesn't apply any conditions to pet's age")
@pytest.mark.update
@pytest.mark.negative
@pytest.mark.parametrize('age',
                         ['-12', generate_str.n_string(255), generate_str.n_string(1000),
                          generate_str.chinese_chars(), generate_str.special_chars()],
                         ids=['negative number', '255 chars', '1000 chars', 'chinese chars', 'special chars'])
def test_invalid_animal_type(get_key, pet_with_image, age, name='Kitty', animal_type='siamese cat'):
    """Check a user can't update one's pet's age with invalid value. """

    # Try to update the pet's info
    status, result = pf.update_pet_info(get_key, pet_with_image['id'], name, animal_type, age)

    assert status == 400


@pytest.mark.skip("By now any user can change other user's pet's info!")
@pytest.mark.update
@pytest.mark.negative
def test_update_other_users_pet(get_key, other_key, name='Kitty', animal_type='siamese cat', age='3'):
    """Check a user can't update other user's pet's info. """

    # Add a pet using other user's key
    _, pet = pf.add_new_pet(other_key, name='Maopang', animal_type='Cat', age='10', pet_photo='images/jpeg_pic.jpeg')

    # Try to update the just creatd other user's pet's info
    status, result = pf.update_pet_info(get_key, pet['id'], name, animal_type, age)

    assert status == 403
