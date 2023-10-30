Task 24.7.2 (Skillfactory online course for Python automated QA)

Pet Friends project (https://petfriends.skillfactory.ru) is an application for Skillfactory online school students practice

REST API swagger documentation can be found on https://petfriends.skillfactory.ru/apidocs/#/

From the previous tasks there's a project containing:

    - api.py file contains REST API methods library corresponding to swagger documentation 

    - file settings.py in root directory contains valid login and password

    - all tests are in test_pet_friends file in /tests directory

    - images for tests are in tests/images/ directory
    

The task:

1. Rewrite the tests written in the previous module so that they use the fixture of getting the API key, 
instead of retrieving it within each individual test.
2. Divide the tests written in the previous module into several groups of functional tests, which are described in 
the ini file. Mark some tests with x_fail, skip labels.
3. Write a decorator that will log requests in API tests. With this decorator, we mark functions that send requests 
to the application under test. After passing the test, a file appears on the hard disk log.txt , in which there are two 
sections: the first lists the request headers, path parameters, string parameters and the request body; the second lists
the response code, the response body.
