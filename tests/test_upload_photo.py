# To run these tests in PyCharm remember to install pytest package
# and to set "pytest" as a Default test runner in Settings->Tools->Python Integrated Tools

import pytest
from api import PetFriends
from settings import valid_email, valid_password
import os
import generate_str

pf = PetFriends()


@pytest.mark.add_photo
@pytest.mark.positive
@pytest.mark.parametrize("pet_photo",
                         ["images/jpg_pic.jpg", "images/jpeg_pic.jpeg",
                          #"images/png_pic.jpg", Currently a png image cannot be added.
                          ],
                         ids=["jpg picture", "jpeg picture"]) #"png image is not allowed
def test_positive(get_key, pet_photo):
     """Check if a user can upload different images to his pet's card without photo."""

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
@pytest.mark.negative
@pytest.mark.parametrize('auth_key',
                         [{'key': ''}, {'key': f'{generate_str.n_string(255)}'},
                          {'key': f'{generate_str.n_string(1000)}'}],
                         ids=['empty str', '255 chars', '1000 chars'])
def test_wrong_key(get_key, auth_key, pet_photo="images/jpeg_pic.jpeg"):
    """Check one cannot upload a photo to pet's card having a wrong auth_key"""

    # Get the absolute path of pet's photo and save it to the pet_photo variable
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Get a list of user's pets my_pets
    _, my_pets = pf.get_pets_list(get_key, "my_pets")

    # Go through my_pets list
    for i in range(0, len(my_pets["pets"])):
        # Find a pet without a photo and try to upload the image to its card
        if my_pets["pets"][i]["pet_photo"] == "":
            status, result = pf.add_pets_photo(auth_key, my_pets["pets"][i]['id'], pet_photo)
            break
        # If there are no pets without a photo then add one, and upload the image to its card
        if i == len(my_pets["pets"]) - 1:
            _, simple_pet = pf.add_new_pet_without_photo(get_key, "Kitty", "cat", "2")
            status, result = pf.add_pets_photo(auth_key, simple_pet['id'], pet_photo)

    assert status == 403


@pytest.mark.add_photo
@pytest.mark.negative
@pytest.mark.parametrize('pet_id',
                         ['', generate_str.n_string(255), generate_str.n_string(1000)],
                         ids=['empty string', '255 chars', '1000 chars'])
def test_wrong_pet_id(get_key, pet_id, pet_photo="images/jpeg_pic.jpeg"):
    """Check one cannot upload jpg image with wrong pet_id and get 404 response status (pet_id is a part of the URL)"""

    # Get the absolute path of pet's photo and save it to the pet_photo variable
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Try to upload a photo with a wrong pet_id
    status, result = pf.add_pets_photo(get_key, pet_id, pet_photo)

    assert status == 404


@pytest.mark.add_photo
@pytest.mark.negative
@pytest.mark.parametrize("pet_photo",
                         ["images/txt.txt", "images/broken_jpeg.jpeg", "images/HD_jpg.jpg"],
                         ids=["txt file", "broken jpeg", "HD image"])
def test_wrong_image_file(get_key, pet_photo):
     """Check requests to upload different types of files instead of jpg image do not cause response code 500."""

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

     assert status != 500
