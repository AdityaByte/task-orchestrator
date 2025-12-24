"""
Functionality:
tasks define with some properties.
task decorator.
"""
from functools import wraps
from task_engine.core.registry import Registry
from task_engine.enums.task_status import TaskStatus

class Task:

    def __init__(self, name, depends_on=None, retries=None, condition=None):
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