import pytest
from api import PetFriends
from settings import valid_email, valid_password


pf = PetFriends()


@pytest.mark.delete
@pytest.mark.positive
def test_positive(get_key):
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
def test_someone_elses_pet(get_key):
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
