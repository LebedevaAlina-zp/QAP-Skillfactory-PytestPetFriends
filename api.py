import json
import datetime
from logged_requests_lib import LoggedRequests, log_filename
import inspect

# Install requests-toolbelt library
from requests_toolbelt.multipart.encoder import MultipartEncoder

def my_api_logs(func):
    """Decorator to write informative logs for API requests"""
    def wrapper(*args, **kwargs):
        time_start = datetime.datetime.now()
        time_start_formatted = time_start.strftime("%Y-%m-%d_%H-%M-%S")
        with open(log_filename, "a+") as log_file:
            log_file.write(f"\n==========================================================================\n")
            # Write into the log file from where the api request function was run
            log_file.write(f"{inspect.currentframe().f_back}\n\n")
            # Write into the log file an api request function's name and time of start
            log_file.write(f"Running {func.__name__} starts at {time_start_formatted}" + "\n\n")
        # Run the api request function
        result = func(*args, **kwargs)
        time_end = datetime.datetime.now()
        run_time = time_end - time_start
        with open(log_filename, "a") as log_file:
            # Write into the log file the api function run time
            log_file.write(f"{func.__name__} completed in {run_time}\n")
        return result
    return wrapper


class PetFriends:
    """REST API library for Pet Friends project (application for Skillfactory online school students practice),
    find swagger documentation on https://petfriends.skillfactory.ru/apidocs/#/"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru"
        self.logged_requests = LoggedRequests()


    @my_api_logs
    def get_api_key(self, email: str, password: str) -> json:
        """To obtain an auth_key the method makes a GET request transmitting user's email and password to the server
        and returns a response status code and a JSON result containing a unique key corresponded to that user"""

        headers = {
            'email': email,
            'password': password
        }

        res = self.logged_requests.get(self.base_url + '/api/key', headers)

        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    @my_api_logs
    def get_pets_list(self, auth_key: json, filter: str = "") -> json:
        """To get a list of pets the method makes a GET request transmitting an auth_key to the server
        and returns a response status and a JSON formatted result containing a list of pets available to the user
        filtered by 'filter' which can take either '' or 'my_pets'. With a filter '' the user gets a list of all pets.
        With a filter 'my_pets' the user gets a list of his pets only"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = self.logged_requests.get(self.base_url + '/api/pets', headers=headers, params=filter)

        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    @my_api_logs
    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """To add a new pet without a photo the method makes a POST request to the server transmitting valid auth_key,
        animal's name, animal_type (for instance, German Shepherd), age
        and returns response status code and json formatted result with created pet's data"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = self.logged_requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    # Copied from dimm23 repository on https://github.com/SkillfactoryCoding/QAP_PetFriensTesting
    # Modified to allow png images as they are allowed by the swagger documentation
    @my_api_logs
    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """To add a new pet the method makes a POST request to the server transmitting valid auth_key,
        animal's name, animal_type (for instance, German Shepherd), age, photo and returns response status code
        and json formatted result with created pet's data
        Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус запроса на сервер и
        результат в формате JSON с данными добавленного питомца"""

        # Detect the format of pet's photo
        image_format = 'image/jpeg' if pet_photo[-4:-1] in ('.jpg', 'jpeg') else 'image/png'

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), image_format)
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = self.logged_requests.post(self.base_url + '/api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    # Copied from dimm23 repository on https://github.com/SkillfactoryCoding/QAP_PetFriensTesting
    @my_api_logs
    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """To delete a pet the method make a DELETE request to the server transmitting valid auth_key and pet's id
        and returns response status code and a JSON result containing a notification of successful deletion.
        By now there's a bug: result contains only an empty string while the status code is still 200.
        Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}

        res = self.logged_requests.delete(self.base_url + '/api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # Copied from dimm23 repository on https://github.com/SkillfactoryCoding/QAP_PetFriensTesting
    @my_api_logs
    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """To update data of existing pet (pet_id) the method makes a PUT request to the server with user's auth_key and
        new pet's data and returns response status code and json formatted result with updated pet's data.
        Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = self.logged_requests.put(self.base_url + '/api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    @my_api_logs
    def add_pets_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """To add a photo to an existing pet (pet_id) that doesn't have one the method makes a POST request
        to the server with user's auth_key and pet's photo in jpg or png format and returns response status code
        and json formatted result with pet's data.
        Метод добавляет фото формата jpg или png к существующей карточке питомца без фото."""

        # Detect the format of pet's photo
        image_format = 'image/jpeg' if pet_photo[-4:-1] in ('.jpg', 'jpeg') else 'image/png'

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), image_format)
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = self.logged_requests.post(self.base_url + f'/api/pets/set_photo/{pet_id}', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result
