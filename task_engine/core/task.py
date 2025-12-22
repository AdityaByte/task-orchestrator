"""
Functionality:
tasks define with some properties.
task decorator.
"""
from functools import wraps
from task_engine.core.registry import Registry
from task_engine.enums.task_status import TaskStatus

class Task:

    def __init__(self, name, depends_on=None, retries=None):
        self.name = name
        self.depends_on = depends_on or []
        self.retries = retries
        self.function_ref = None
        self.function_args = {}
        self.function_kwargs = {}
        self.executed = False
        self.state = TaskStatus.PENDING # Default state

    def __call__(self, original_function):

        self.function_ref = original_function # Saving the function reference.

        # Registering task immediately.
        Registry.set_task(self.name or original_function.__name__, self)

        @wraps(original_function)
        def wrapper(*args, **kwargs):
            # Since i have to keep save the args and keyword args too.
            self.function_args = args
            self.function_kwargs = kwargs
            return original_function(*args, **kwargs)

        return wrapper