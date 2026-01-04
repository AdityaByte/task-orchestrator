from pravaha.core.task import Task
from pravaha.retry.policy import RetryPolicy
from pravaha.retry.backoff import fixed_delay
from pravaha.core.executor import TaskExecutor

class ConnectionError(Exception):
    pass

counter = {"value": 0}

@Task(name="make_db_connection", retries=RetryPolicy(max_retries=3, backoff=fixed_delay(3), retry_on=(ConnectionError, )))
def make_db_connection():
    if counter['value'] == 2:
        print("Connection made")
        return
    counter['value'] += 1
    raise ConnectionError("Connection error.")

@Task(name="fetch_data_from_db", depends_on=['make_db_connection'])
def fetch_data_from_db():
    print("Fetching data from db.")
    return "Hello world"

@Task(name="print_data", depends_on=['fetch_data_from_db'])
def print_data(data):
    print("Printing data")
    print(data)

if __name__ == '__main__':
    TaskExecutor.execute()