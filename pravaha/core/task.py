"""
Functionality:
tasks define with some properties.
task decorator.
"""
from functools import wraps
from pravaha.core.registry import Registry
from pravaha.enums.task_status import TaskStatus
from pravaha.retry.policy import RetryPolicy
from pravaha.enums.task_priority import TaskPriority

class Task:
    """
    Represents a unit of work in the workflow engine.

    Args:
        name (str): Name of the task.
        depends_on (list[str]): List of task dependencies.
        retries (RetryPolicy): Takes the retry policy in which max retries and backoff function and retry_on can be defined.
        condition (Lambda Function | Condition functions): Executing the task when the condition evaluated to True.
        priority (TaskPriority): Priority of task.
        tag (str): Tag to the task.
    """

    def __init__(self, name, depends_on=None, retries: RetryPolicy=None, condition=None, priority=TaskPriority.NORMAL, tag=None):
        self.name = name
        self.depends_on = depends_on or []
        self.retries = retries
        self.function_ref = None
        self.state = TaskStatus.PENDING # Default state
        self.start_time = ""
        self.end_time = ""
        self.duration = None
        self.error = None
        # Adding a new functionality condition based task execution.
        if condition is not None and not callable(condition):
            raise TypeError("Condition must be callable.")
        self.condition = condition
        self.priority = priority
        self.tag = tag

    def __call__(self, original_function):

        self.function_ref = original_function # Saving the function reference.

        # Registering task immediately.
        Registry.set_task(self.name or original_function.__name__, self)

        @wraps(original_function)
        def wrapper(*args, **kwargs):
            print(f"Wrapper run by this function: {original_function.__name__}")
            # Since i have to keep save the args and keyword args too.
            return original_function(*args, **kwargs)

        return wrapper

class ErrorInformation:
    """
    If error came to a task this class holds all the data related to the error.
    - Type of the error.
    - Name of the error (eg: ValueError)
    - Error message.
    """

    def __init__(self, exception: Exception):
        self.exception = exception
        self.error_type = type(exception)
        self.error_name = self.error_type.__name__
        self.error_msg = str(exception)

    def get_error_type(self):
        return self.error_type

    def get_error_name(self):
        return self.error_name

    def get_error_msg(self):
        return self.error_msg