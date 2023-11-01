import pytest
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

@pytest.mark.add_simple
@pytest.mark.positive
def test_valid_data(get_key, name="Kitty", animal_type="The Kitten", age="0"):
    """Check a user can add a pet with valid data without a photo correctly."""

    # Add a new pet without a photo
    status, result = pf.add_new_pet_without_photo(get_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age
