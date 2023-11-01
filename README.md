Pet Friends project (https://petfriends.skillfactory.ru) is an application for Skillfactory online school students practice

Here's a project for REST API testing of PetFriends app with pytest written for an online course for Python automated QA

REST API swagger documentation can be found on https://petfriends.skillfactory.ru/apidocs/#/

The structure of the project

    - api.py file contains REST API methods library corresponding to the swagger documentation 

    - file settings.py in root directory contains valid login and password

    - all tests are in /tests directory

    - desccription of tests groups can be found in pytest.ini file

    - images for tests are in tests/images/ directory

    - logged_requests_lib configures api requests information to be written in logs/ directory while test running
    

Here's the sequence of tasks during the online course:

1. Complete existing API library api.py with all the other methods from swagger documentation
2. Rewrite the tests written in the previous module so that they use a getting an API key fixture, 
instead of retrieving it within each individual test.
2. Divide the tests written in the previous module into several groups of functional tests, which are described in 
the ini file. Mark some tests with x_fail, skip labels.
3. Write a decorator that will log requests in API tests. With this decorator, we mark functions that send requests 
to the application under test. After passing the test, a file appears on the hard disk log.txt , which contains: 
the request headers, path parameters, string parameters and the body; the response code and body.
4. Devide the code of the tests into separate  test files according to their functionality.
5. Parametrize the tests existing: API requests parameters for positive and negative cases, headers Accept and Content-type
