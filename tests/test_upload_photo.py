# To run these tests in PyCharm remember to install pytest package
# and to set "pytest" as a Default test runner in Settings->Tools->Python Integrated Tools

import pytest
from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


@pytest.mark.add_photo
@pytest.mark.positive
def test_jpg(get_key, pet_photo="images/0zA6-Cc4OL0.jpg"):
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
def test_jpeg(get_key, pet_photo="images/cat1.jpeg"):
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
def test_png(get_key, pet_photo="images/dfslkahg.png"):
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
