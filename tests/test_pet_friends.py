# To run these tests in PyCharm remember to install pytest package
# and to set "pytest" as a Default test runner in Settings->Tools->Python Integrated Tools

import pytest
from api import PetFriends
from settings import valid_email, valid_password
import os


pf = PetFriends()

@pytest.mark.key
@pytest.mark.positive
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Check a valid user can get an auth_key using get_api_key method, make sure status code is 200 and the response
    contains 'key' """

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

@pytest.mark.key
@pytest.mark.negative
def test_get_api_key_with_wrong_password(email=valid_email, password=valid_password+"0"):
    """Check a user can't get an auth_key using get_api_key method with a wrong password"""

    #Make a request and save a resposponse status
    status, _ = pf.get_api_key(email, password)

    #Check the response status code is 403
    assert status == 403

@pytest.mark.key
@pytest.mark.positive
def test_get_api_key_with_uppercase_email(email=valid_email.upper(), password=valid_password):
    """Check a user still gets an auth_key, providing a valid but written uppercase name and a valid password"""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result

@pytest.mark.key
@pytest.mark.negative
def test_get_api_key_with_uppercase_password(email=valid_email, password=valid_password.upper()):
    """Check a user can't get an auth_key, roviding a valid name and a valid but by mistake written uppercase password"""

    status, _ = pf.get_api_key(email, password)

    assert status == 403

@pytest.mark.list
@pytest.mark.positive
def test_get_all_pets_list_with_valid_key(get_key, filter=''):
    """Check the response status is 200 and the result contains a non-empty list of pets when a request via
    get_pets_list method with empty filter is made"""

    status, result = pf.get_pets_list(get_key, filter)
    assert status == 200
    assert 'pets' in result
    assert len(result['pets']) > 0

@pytest.mark.list
@pytest.mark.positive
def test_get_pets_list_with_filter_my_pets(get_key, filter="my_pets"):
    """Check that for a request for pets list with 'my_pets' filter the response has got non-empty list of pets.
     Проверяем что запрос питомцев с фильтром "my_pets" возвращает непустой список питомцев."""

    status, result = pf.get_pets_list(get_key, "my_pets")

    assert status == 200
    assert len(result['pets']) > 0

@pytest.mark.list
@pytest.mark.negative
def test_get_all_pets_with_wrong_key(get_key, filter=''):
    """Check a user can't get a list of pets with a wrong auth_key."""

    # Delete the last symbol in the key obtained
    wrong_key = get_key.copy()
    wrong_key['key'] = wrong_key['key'][:-1]

    status, result = pf.get_pets_list(wrong_key, filter)

    assert status == 403

@pytest.mark.add_pet
@pytest.mark.positive
def test_add_new_pet_with_valid_data(get_key, name='Carrie', animal_type='siamese cat',
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
def test_add_new_pet_with_valid_data_rus(get_key, name='Барбоскин', animal_type='двортерьер',
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
def test_add_new_pet_with_wrong_key(get_key, name='Carrie', animal_type='siamese cat',
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
def test_add_new_pet_with_png_image(get_key, name='Grusha', animal_type='cockatiel',
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

@pytest.mark.update
@pytest.mark.positive
@pytest.mark.skip(reason="Currently russian characters are not allowed.")
def test_successful_update_self_pet_info(get_key, name='Мурзик', animal_type='Котэ', age='5'):
    """Check a user can update one's pet's data correctly."""

    # Get the user's pets list
    _, my_pets = pf.get_pets_list(get_key, "my_pets")

    # If the list is empty add a new pet
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(get_key, 'Alice', 'Cat', '3')

    # Try to update the data of the first pet in the list
    status, result = pf.update_pet_info(get_key, my_pets['pets'][0]['id'], name, animal_type, age)

    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age

@pytest.mark.delete
@pytest.mark.positive
def test_successful_delete_self_pet(get_key):
    """Check a user can delete one's pet."""

    # Get an auth_key and a list of user's pets
    _, my_pets = pf.get_pets_list(get_key, "my_pets")

    # If the list is empty add a new pet and request the list of user's pet once again
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(get_key, "Pettypet", "bird", "3", "images/cat1.jpeg")
        _, my_pets = pf.get_pets_list(get_key, "my_pets")

    # Save the id of the first pet in the list in pet_id and try to delete one
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(get_key, pet_id)

    # Get the list of user's pets one more time
    _, my_pets = pf.get_pets_list(get_key, "my_pets")

    # Check the status code for delete request is 200
    # and the list of pets doesn't contain a pet with pet_id anymore
    assert status == 200
    assert pet_id not in my_pets.values()

@pytest.mark.delete
@pytest.mark.negative
@pytest.mark.skip(reason="Currently any user can delete someone else's pet. The test is not polite with other user's "
                         "pet deletion =(( It should be changed: another user adds a new pet and then main user tries"
                         " to delete it.")
def test_delete_someone_elses_pet(get_key):
    """Check a user cannot delete someone else's pet (not from "my_pets" pets list)"""

    # !!!Attention! Bug found here. A user actually can delete someone else's pet.

    # Get a list of all the pets all_pets and a list of user's pets my_pets.
    _, all_pets = pf.get_pets_list(get_key, '')
    _, my_pets = pf.get_pets_list(get_key, 'my_pets')

    # If all_pets and my_pets lists are of the same length (there are no pets of other users) then raise an Ecxeption
    if len(my_pets['pets']) == len(all_pets['pets']):
        raise Exception("There are no other users' pets.")

    # Now find a pet from all_pets list that is not in my_pets
    # Save the id of the first pet in all_pets list into pet_id variable.
    i = 0
    pet_id = all_pets['pets'][i]['id']

    # If my_pets is not empty then:
    if len(my_pets['pets']) != 0:
        # Check the pet with pet_id is not in my_pets list
        for pet in my_pets['pets']:
            # And if it is then take the next pet from all_pets list and check it's not in my_pets list in another loop
            if pet['id'] == pet_id:
                i += 1
                pet_id = all_pets['pets'][i]['id']

    # Try to delete someone else's pet
    status, _ = pf.delete_pet(get_key, pet_id)

    # Check the deletion was unsuccessful: status code is not 200 and a pet with pet_id is still in all_pets list
    assert status != 200
    assert pet_id in all_pets['pets'].values()

@pytest.mark.add_simple
@pytest.mark.positive
def test_add_new_pet_without_photo_with_valid_data(get_key, name="Kitty", animal_type="The Kitten", age="0"):
    """Check a user can add a pet with valid data without a photo correctly."""

    # Add a new pet without a photo
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age

@pytest.mark.add_photo
@pytest.mark.positive
def test_upload_photo_to_pets_card_jpg(get_key, pet_photo="images/0zA6-Cc4OL0.jpg"):
     """Check if a user can upload jpg image to his pet's card which lacks of photo."""

     # Get the absolute path of pet's photo and save it to the pet_photo variable
     pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

     # Get a list of user's pets my_pets
     _, my_pets = pf.get_pets_list(get_key, "my_pets")

     # Go through my_pets list
     for i in range(0, len(my_pets["pets"])):
         # Find a pet without a photo and try to upload the image to its card
         if my_pets["pets"][i]["pet_photo"] == "":
             status, result = pf.add_pets_photo(get_key, my_pets["pets"][i]['id'], pet_photo)
             break
         # If there are no pets without a photo then add one, and upload the image to its card
         if i == len(my_pets["pets"]) -1:
             _, simple_pet = pf.add_new_pet_without_photo(get_key, "Kitty", "cat", "2")
             status, result = pf.add_pets_photo(get_key, simple_pet['id'], pet_photo)

     assert status == 200
     assert result['pet_photo'] != ""

@pytest.mark.add_photo
@pytest.mark.positive
def test_upload_photo_to_pets_card_jpeg(get_key, pet_photo="images/cat1.jpeg"):
    """Check if a user can upload jpg image to his pet's card which lacks of photo"""

    # Get the absolute path of pet's photo and save it to the pet_photo variable
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Get a list of user's pets my_pets
    _, my_pets = pf.get_pets_list(get_key, "my_pets")

    # Go through my_pets list
    for i in range(0, len(my_pets["pets"])):
        # Find a pet without a photo and try to upload the image to its card
        if my_pets["pets"][i]["pet_photo"] == "":
            status, result = pf.add_pets_photo(get_key, my_pets["pets"][i]['id'], pet_photo)
            break
        # If there are no pets without a photo then add one, and upload the image to its card
        if i == len(my_pets["pets"]) - 1:
            _, simple_pet = pf.add_new_pet_without_photo(get_key, "Kitty", "cat", "2")
            status, result = pf.add_pets_photo(get_key, simple_pet['id'], pet_photo)

    assert status == 200
    assert result['pet_photo'] != ""

@pytest.mark.add_photo
@pytest.mark.positive
@pytest.mark.skip(reason="Currently a pet with a png image can't be added.")
def test_upload_photo_to_pets_card_png(get_key, pet_photo="images/dfslkahg.png"):
    """Check if a user can upload jpg image to his pet's card which lacks of photo"""

    #！！！Attention!！！ Bug found here. A png image cannot be uploaded despite what's said in swagger docs.

    # Get the absolute path of pet's photo and save it to the pet_photo variable
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Get an auth_key and a list of user's pets my_pets
    _, my_pets = pf.get_pets_list(get_key, "my_pets")

    # Go through my_pets list
    for i in range(0, len(my_pets["pets"])):
        # Find a pet without a photo and try to upload the image to its card
        if my_pets["pets"][i]["pet_photo"] == "":
            status, result = pf.add_pets_photo(get_key, my_pets["pets"][i]['id'], pet_photo)
            break
        # If there are no pets without a photo then add one, and upload the image to its card
        if i == len(my_pets["pets"]) - 1:
            _, simple_pet = pf.add_new_pet_without_photo(get_key, "Kitty", "cat", "2")
            status, result = pf.add_pets_photo(get_key, simple_pet['id'], pet_photo)

    assert status == 200
    assert result['pet_photo'] != ""
