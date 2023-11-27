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
                         ["images/jpg_pic.jpg", "images/jpeg_pic.jpeg", "images/HD_jpg.jpg",
                          #"images/png_pic.jpg", Currently a png image cannot be added.
                          ],
                         ids=["jpg picture", "jpeg picture", "HD image"]) #"png image is not allowed
def test_positive(get_key, pet_photo):
     """Check if a user can upload different images to his pet's card without photo."""

     # Get the absolute path of pet's photo and save it to the pet_photo variable
     pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

     # Add a pet without a photo, then upload the image to its card
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

    # Add a pet without a photo
    _, simple_pet = pf.add_new_pet_without_photo(get_key, "Kitty", "cat", "2")

    # Try to upload the image to its card using wrong auth_key
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
                         ["images/txt.txt", "images/broken_jpeg.jpeg"],
                         ids=["txt file", "broken jpeg"])
def test_wrong_image_file(get_key, pet_photo):
     """Check requests to upload different types of files instead of jpg image get 400 response status code.."""

     # Get the absolute path of pet's photo and save it to the pet_photo variable
     pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

     # Add a pet without a photo, then upload the image to its card
     _, simple_pet = pf.add_new_pet_without_photo(get_key, "Kitty", "cat", "2")
     status, result = pf.add_pets_photo(get_key, simple_pet['id'], pet_photo)

     assert status == 400


@pytest.mark.add_photo
@pytest.mark.negative
def test_upload_other_users_pet_photo(get_key, other_key, pet_photo="images/jpeg_pic.jpeg"):
     """Check that a user cannot upload a photo to other user's pet's card."""

     # Get the absolute path of pet's photo and save it to the pet_photo variable
     pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

     # Add a pet without a photo for the other user, then upload the image to its card
     _, simple_pet = pf.add_new_pet_without_photo(other_key, "Kitty", "cat", "2")
     status, result = pf.add_pets_photo(get_key, simple_pet['id'], pet_photo)

     assert status == 403


@pytest.mark.add_photo
@pytest.mark.negative
def test_upload_one_more_pet_photo(get_key, pet_with_image, pet_photo="images/jpeg_pic.jpeg"):
     """Check one cannot upload a photo to a pet's card that already has a photo."""

     # Get the absolute path of pet's photo and save it to the pet_photo variable
     pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

     # Try to upload the image to a pet's card with the image
     status, result = pf.add_pets_photo(get_key, pet_with_image, pet_photo)

     assert status == 400
