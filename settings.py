import os
# Install python-dotenv library
from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

other_email = os.getenv('other_email')
other_password = os.getenv('other_password')
