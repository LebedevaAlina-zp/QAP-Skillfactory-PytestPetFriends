import pytest
from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


@pytest.mark.update
@pytest.mark.positive
def test_valid_data(get_key, name='Meimei', animal_type='Mao', age='5'):
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
