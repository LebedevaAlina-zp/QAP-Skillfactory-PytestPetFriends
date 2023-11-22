import pytest
from api import PetFriends
from settings import valid_email, valid_password
import generate_str


pf = PetFriends()


@pytest.mark.delete
@pytest.mark.positive
def test_positive(get_key):
    """Check a user can delete one's pet."""

    # Get an auth_key and a list of user's pets
    _, my_pets = pf.get_pets_list(get_key, "my_pets")

    # If the list is empty add a new pet and request the list of user's pet once again
    if len(my_pets['pets']) == 0:
        _, new_pet = pf.add_new_pet(get_key, "Pettypet", "bird", "3", "images/cat1.jpeg")
        my_pets = {'pets':[new_pet]}

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
@pytest.mark.parametrize('pet_id',
                         ['', generate_str.n_string(255), generate_str.n_string(1000)],
                         ids=['empty string', '255 chars', '1000 chars'])
def test_wrong_pet_id(get_key, pet_id):
    """Check a user get a 404 pesponse status for delete request with wrong pet_id value as it's a part of the request URL."""

    status, _ = pf.delete_pet(get_key, pet_id)

    assert status == 404


@pytest.mark.delete
@pytest.mark.negative
@pytest.mark.skip(reason="Currently any user can delete someone else's pet. The test is not polite with other user's "
                         "pet deletion =(( It should be changed: another user adds a new pet and then main user tries"
                         " to delete it.")
@pytest.mark.parametrize('image', [0, 1], ids=['pet without photo', 'pet with a photo'])
def test_someone_elses_pet(get_key, other_key, image):
    """Check a user cannot delete someone else's pet (not from "my_pets" pets list)"""

    # Add a pet using other's user auth key
    if image == 0:
        _, pet = pf.add_new_pet_without_photo(other_key, 'Alice', 'Cat', '3')
    else:
        _, pet = pf.add_new_pet(other_key, 'Alice', 'Cat', '3', 'images/jpg_pic.jpg')

    # Try to delete someone else's pet
    status, _ = pf.delete_pet(get_key, pet['id'])

    # Get a list of all the pets all_pets and a list of user's pets my_pets.
    _, other_user_pets = pf.get_pets_list(other_key, 'my_pets')

    # Check the deletion was unsuccessful: status code is 403 and a pet with pet_id is still in all_pets list
    assert status == 403
    assert other_pet['id'] in other_user_pets.values()


@pytest.mark.delete
@pytest.mark.negative
@pytest.mark.parametrize('auth_key',
                         [{'key': ''}, {'key': f'{generate_str.n_string(255)}'},
                          {'key': f'{generate_str.n_string(1000)}'}],
                         ids=['empty str', '255 chars', '1000 chars'])
def test_wrong_key(get_key, auth_key):
    ''' Check one cannot delete a pet having a wrong auth_key'''

    # First add a pet
    _, new_pet = pf.add_new_pet_without_photo(get_key, "Pettypet", "bird", "3")
    pet_id = new_pet['id']

    # Try to delete it
    status, _ = pf.delete_pet(auth_key, pet_id)

    assert status == 403