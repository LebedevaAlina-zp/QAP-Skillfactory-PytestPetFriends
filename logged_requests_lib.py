import datetime
import requests
import inspect
import codecs

# create a logfile's name
current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"../logs/log_{formatted_datetime}.txt"


def requests_logs(func):
    """Decorator to write informative logs for API requests"""
    def wrapper_logs(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        indent = 9*' '
        args_names_list = str(inspect.signature(func))[1:-1].split(', ')
        args_values = args_repr + kwargs_repr
        with codecs.open(log_filename, "a+", 'utf-8') as log_file:
            # Write the request parameters to a log file
            log_file.write(f"Request:\n")
            log_file.write(f"{indent}Method: {func.__name__.upper()}\n")
            for i in range(1, len(args_values)):
                log_file.write(f"{indent}" + f"{str(args_names_list[i].split('=')[0]).upper()}: ")
                log_file.write(f"{args_values[i]}\n")
                for i in range(len(args_values) + 1, len(args_names_list)):
                    log_file.write(f"{indent}" + f"{str(args_names_list[i].split('=')[0]).upper()}: No")

        result = func(*args, **kwargs)

        with open(log_filename, "a+") as log_file:
            # Write the response parameters to a log file
            log_file.write(f"Response:\n")
            log_file.write(f"{indent}" + f"Status Code: {result.status_code},\n")
            log_file.write(f"{indent}" + f"Response Data: {result.text[:200]}\n\n") #Printing first 200 result characters

        return result
    return wrapper_logs


class LoggedRequests:

    @requests_logs
    def get(self, url, headers, params={}):
        res = requests.get(url, headers=headers, params=params)
        return res

    @requests_logs
    def post(self, url, headers, data={}):
        res = requests.post(url, headers=headers, data=data)
        return res

    @requests_logs
    def put(self, url, headers, data={}):
        res = requests.put(url, headers=headers, data=data)
        return res

    @requests_logs
    def delete(self, url, headers):
        res = requests.delete(url, headers=headers)
        return res