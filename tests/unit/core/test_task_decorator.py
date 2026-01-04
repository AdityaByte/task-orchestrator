from pravaha.core.task import Task
from pravaha.core.registry import Registry

def test_task_decorator_assigns_function_reference():

    @Task(name="my_task")
    def my_task():
        pass

    saved_task: Task = Registry.get_task()["my_task"]
    """In the task @wraps wraps the original function to a wrapper so if you do something like this
    assert saved_task.function_ref (original_function reference) == my_task (wrapper function reference because we are returning
    that from the call function)
    
    So this fails up now we have to check via the my_task.__wrapped__ property it gives the original_function reference."""
    assert saved_task.function_ref is my_task.__wrapped__


def test_task_is_registered_in_registry_on_decoration():

    @Task(name="task1")
    def task1():
        pass

    assert Registry.get_task()["task1"] is not None

def test_task_decorator_returns_callable_wrapper():

    @Task(name="task1")
    def task1():
        return "Task1"

    assert callable(task1)

def test_task_wrapper_executes_original_function():

    @Task(name="task1")
    def task1():
        return "Task1"

    assert task1() == "Task1"

def test_task_wrapper_forwards_arguments_correctly():

    @Task(name="task1")
    def task1(name):
        return f"My name is {name}"

    assert task1("Aditya") == "My name is Aditya"

def test_task_preserves_function_metadata():

    @Task(name="task1")
    def task1(name):
        """This is docstring"""
        pass

    assert task1.__name__ == "task1"
    assert task1.__doc__ == "This is docstring"
    assert hasattr(task1, "__wrapped__")
