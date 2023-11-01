import pytest
from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

@pytest.mark.add_pet
@pytest.mark.positive
def test_valid_data(get_key, name='Carrie', animal_type='siamese cat',
                                     age='8', pet_photo='images/0zA6-Cc4OL0.jpg'):
    """Check a pet with valid data can be added correctly."""

    # Get the absolute path of pet's photo and save it to the pet_photo variable
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Add a new pet
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

@pytest.mark.add_pet
@pytest.mark.positive
@pytest.mark.skip(reason="Currently russian characters are not allowed.")
def test_valid_data_rus(get_key, name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpeg'):
    """Check pet with typed in Russian valid data can be added correctly."""

    # Get the absolute path of pet's photo and save it to the pet_photo variable
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Add a new pet
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age

@pytest.mark.add_pet
@pytest.mark.negative
def test_wrong_key(get_key, name='Carrie', animal_type='siamese cat',
                                     age='8', pet_photo='images/0zA6-Cc4OL0.jpg'):
    """Check a user can't add a new pet with a wrong auth_key."""

    # Get the absolute path of pet's photo and save it to the pet_photo variable
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Delete the last symbol in the key obtained
    wrong_key = get_key.copy()
    wrong_key['key'] = wrong_key['key'][:-1]

    # Try to add a new pet
    status, result = pf.add_new_pet(wrong_key, name, animal_type, age, pet_photo)

    assert status == 403

@pytest.mark.add_pet
@pytest.mark.positive
@pytest.mark.skip(reason="Currently a pet with a png image can't be added.")
def test_png_image(get_key, name='Grusha', animal_type='cockatiel',
                                  age='5', pet_photo='images/parrot-898.png'):
    """Check if it's possible to add a pet with png image (such an option is included to swagger documentation)."""

    #!!!Attention! Bug found here. A pet with a png image can't be added despite this option is provided by swagger docs.

    # Get the absolute path of pet's photo and save it to the pet_photo variable
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

   # Try to add a new pet
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age \
           and result['pet_photo'] != '', "A pet hasn't been added properly"
