Retry Policy
============

Sometimes tasks fail due to temporary issues such as network errors.
Task Orchestrator allows you to **automate retry logic** for tasks using
the built-in ``RetryPolicy`` module.

With ``RetryPolicy``, you can configure:

- **Max Retries**: The maximum number of times a task should be retried.
- **Backoff**: A function controlling the wait time between retries.
  The backoff functions are available in ``task_engine.retry.backoff``.
- **retry_on**: A tuple of exception types. The retry logic will only
  trigger if the task raises one of these exceptions.

This allows tasks to automatically recover from transient failures
without manual intervention.

Example Usage
-------------

.. code-block:: python

   from task_engine.core.task import Task
   from task_engine.retry.policy import RetryPolicy
   from task_engine.retry.backoff import fixed_delay
   from task_engine.core.executor import TaskExecutor

   # Custom exception for demonstration
   class ConnectionError(Exception):
       pass

   counter = {"value": 0}

   @Task(
       name="make_db_connection",
       retries=RetryPolicy(
           max_retries=3,
           backoff=fixed_delay(3),
           retry_on=(ConnectionError,)
       )
   )
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

Expected Output
---------------

.. code-block:: console

   [RETRY] make_db_connection attempt 1, retrying in 3s
   [RETRY] make_db_connection attempt 2, retrying in 3s
   Connection made
   Fetching data from db.
   Printing data
   Hello world

Notes
-----

- Retry attempts respect the **task registration order**.
- Backoff functions can be customized (fixed, exponential, or custom functions).
- Only exceptions listed in ``retry_on`` trigger retries; other exceptions
  will fail immediately.
