import pytest
from api import PetFriends
from settings import valid_email, valid_password
import os
import generate_str

pf = PetFriends()

@pytest.mark.add_pet
@pytest.mark.positive
@pytest.mark.parametrize('name',
                         ['Carrie', 'Мурзик', '猫猫',
                                  generate_str.n_string(255), '1900', '', generate_str.special_chars()
                                  ],
                         ids=['English name', 'Russian name', 'Chinese name',
                              '255 chars name', 'number name', 'empty name', 'special chars name'])
def test_valid_name(get_key, name, animal_type='siamese cat',
                                     age='2', pet_photo='images/jpg_pic.jpg'):
    """Check a pet with various valid names can be added correctly."""

    # Get the absolute path of pet's photo and save it to the pet_photo variable
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Add a new pet
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age \
           and result['pet_photo'] != ''


@pytest.mark.add_pet
@pytest.mark.positive
@pytest.mark.parametrize('animal_type',
                         ['siamese cat', 'сиамская кошка', '暹罗猫',
                          generate_str.n_string(255), '123', '', generate_str.special_chars()],
                         ids=['english animal type', 'russian animal type', 'chinese animal type',
                              '255 chars animal type', 'number animal type', 'empty animal type',
                              'special chars animal type'])
def test_valid_animal_type(get_key, animal_type, name='Kitty',
                                     age='0', pet_photo='images/jpg_pic.jpg'):
    """Check a pet with various valid animal types can be added correctly."""

    # Get the absolute path of pet's photo and save it to the pet_photo variable
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Add a new pet
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age \
           and result['pet_photo'] != ''


@pytest.mark.add_pet
@pytest.mark.positive
@pytest.mark.parametrize('age',
                         ['2', ' 3 ', '0', '', '3.5', '5.2',],
                         ids=['int age', 'int age with spaces', '0 age',
                              'empty age','noninteger age with a dot', 'noninteger age with a coma'])
def test_valid_age(get_key, age, name='Kitty',
                                     animal_type='siamese cat', pet_photo='images/jpg_pic.jpg'):
    """Check a pet of various ages can be added correctly."""

    # Get the absolute path of pet's photo and save it to the pet_photo variable
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Add a new pet
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age \
           and result['pet_photo'] != ''


@pytest.mark.add_pet
@pytest.mark.positive
@pytest.mark.parametrize('pet_photo',
                         ['images/jpg_pic.jpg', 'images/jpeg_pic.jpeg',
                          #"images/png_pic.png", #Currently a png image cannot be added.
                          'images/HD_jpg.jpg'],
                         ids=['jpg picture', 'jpeg picture', #'png picture', #"png image is not allowed
                              'HD jpg image'])
def test_valid_pet_photo(get_key, pet_photo, name='Kitty', animal_type='siamese cat',
                                     age='0'):
    """Check a pet with various valid images for a pet's photo can be added correctly."""

    # Get the absolute path of pet's photo and save it to the pet_photo variable
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Add a new pet
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age \
           and result['pet_photo'] != ''

@pytest.mark.add_pet
@pytest.mark.negative
@pytest.mark.parametrize('auth_key',
                         [{'key': ''}, {'key': f'{generate_str.n_string(255)}'},
                          {'key': f'{generate_str.n_string(1000)}'}],
                         ids=['empty str', '255 chars', '1000 chars'])
def test_wrong_key(auth_key, name='Carrie', animal_type='siamese cat',age='8', pet_photo='images/jpg_pic.jpg'):
    """Check a user can't add a new pet with a wrong auth_key and have a response 403 statuc code."""

    # Get the absolute path of pet's photo and save it to the pet_photo variable
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Try to add a new pet
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403


@pytest.mark.skip(reason="This tests fail because the application doesn't apply any conditions to pet's name")
@pytest.mark.negative
@pytest.mark.parametrize('name',
                         [generate_str.n_string(1000)],
                         ids=['1000 chars'])
def test_invalid_name(get_key, name, animal_type="Kitten", age="0", pet_photo='images/jpg_pic.jpg'):
    """Check a user can't add a pet with incorrect values for pet's name, and get a server rensponse 400 but not 500."""

    # Add a new pet
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    assert status == 400


@pytest.mark.skip(reason="This tests fail because the application doesn't apply any conditions to pet's animal_type")
@pytest.mark.add_pet
@pytest.mark.negative
@pytest.mark.parametrize('animal_type',
                         [generate_str.n_string(1000)],
                         ids=['1000 chars'])
def test_invalid_animal_type(get_key, animal_type, name='Whitney', age="0", pet_photo='images/jpg_pic.jpg'):
    """Check a user can't add a pet with incorrect values for animal type, and get a server rensponse 400 but not 500."""

    # Add a new pet without a photo
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    assert status == 400


@pytest.mark.skip(reason="This tests fail because the application doesn't apply any conditions to pet's age and treat "
                         "this input parameter as a usual string.")
@pytest.mark.add_pet
@pytest.mark.negative
@pytest.mark.parametrize('age',
                         ['-12', generate_str.n_string(255), generate_str.n_string(1000),
                          generate_str.chinese_chars(), generate_str.special_chars()],
                         ids=['negative number', '255 chars', '1000 chars', 'chinese chars', 'special chars'])
def test_invalid_age(get_key, age, name="Kitty", animal_type="Kitten", pet_photo='images/jpg_pic.jpg'):
    """Check a user can't add a pet with incorrect values for pet's age, and get a server rensponse 400 but not 500."""

    # Add a new pet
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    assert status == 400


@pytest.mark.add_pet
@pytest.mark.negative
@pytest.mark.parametrize("pet_photo",
                         ["images/txt.txt", "images/broken_jpeg.jpeg"],
                         ids=["txt file", "broken jpeg"])
def test_invalid_image_file(get_key, pet_photo, name="Kitty", animal_type="Kitten", age='3'):
    """Check when adding a pet with different types of invalid images application adds a pet without image but
    all the rest data is correct."""

    # Add a new pet
    status, result = pf.add_new_pet(get_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age \
           and result['pet_photo'] == ''
