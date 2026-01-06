from pravaha.core.task import Task
from pravaha.core.executor import TaskExecutor
from pravaha.enums.task_status import TaskStatus
from pravaha.core.registry import Registry
from pravaha.exception.task import TaskNotFoundError
from pravaha.exception.validation import MissingDependencyError
from pravaha.dependency.dependency import Dependency
import pytest

def test_selecting_task_includes_all_dependencies():

    @Task("a", depends_on=['b'])
    def a():
        pass

    @Task("b")
    def b():
        pass

    @Task("c")
    def c():
        pass

    # Selecting the a task only.
    TaskExecutor.execute(taskgroup=("a", ))

    tasks = Registry.get_task()

    assert tasks['a'].state == TaskStatus.SUCCESS
    assert tasks['b'].state == TaskStatus.SUCCESS
    assert tasks['c'].state == TaskStatus.PENDING

def test_multiple_selected_tasks_merge_dependencies():

    exec_count = {'a': 0}

    @Task("a")
    def a():
        exec_count['a'] += 1
        pass

    @Task("b", depends_on=['a'])
    def b():
        pass

    @Task("c", depends_on=['a'])
    def c():
        pass

    @Task("d")
    def d():
        pass

    TaskExecutor.execute(taskgroup=('b', 'c'))

    tasks = Registry.get_task()

    assert tasks['a'].state == TaskStatus.SUCCESS
    assert tasks['b'].state == TaskStatus.SUCCESS
    assert tasks['c'].state == TaskStatus.SUCCESS
    assert tasks['d'].state == TaskStatus.PENDING
    assert exec_count['a'] == 1

def test_missing_task_in_task_group_raises_error():

    @Task("a")
    def a():
        pass

    with pytest.raises(TaskNotFoundError):
        # The task b is missing so it will raise an error.
        TaskExecutor.execute(taskgroup=("a", "b"))

def test_task_a_succeeds_if_any_or_dependency_succeeds():

    @Task("a", depends_on=Dependency("OR", ['b', 'c']))
    def a(val: str):
        print("a", val, sep="\n")

    @Task("b")
    def b():
        raise ValueError("Value error")

    @Task("c")
    def c():
        return "c"

    TaskExecutor.execute()

    tasks = Registry.get_task()

    assert tasks['a'].state == TaskStatus.SUCCESS
    assert tasks['b'].state == TaskStatus.FAILED
    assert tasks['c'].state == TaskStatus.SUCCESS

    assert TaskExecutor.ExecutionContext.get('c') == "c"

def test_and_dependency_fails_if_one_fails():

    @Task("a", depends_on=Dependency("AND", ['b', 'c']))
    def a(val: str):
        print("a", val, sep="\n")

    @Task("b")
    def b():
        raise ValueError("Value error")

    @Task("c")
    def c():
        return "c"

    TaskExecutor.execute()

    tasks = Registry.get_task()

    assert tasks['a'].state == TaskStatus.SKIPPED
    assert tasks['b'].state == TaskStatus.FAILED
    assert tasks['c'].state == TaskStatus.SUCCESS

def test_or_dependency_raises_missing_dependecy_error():

    @Task("a", depends_on=Dependency("OR", ["b"]))
    def a():
        pass

    with pytest.raises(MissingDependencyError):
        TaskExecutor.execute()

def test_or_dependency_skips_task_when_all_dependencies_fail():

    @Task("a", depends_on=Dependency("OR", ['b', 'c']))
    def a():
        pass

    @Task("b")
    def b():
        raise TypeError("type-error")

    @Task("c")
    def c():
        raise ValueError("value-error")

    TaskExecutor.execute()

    tasks = Registry.get_task()

    assert tasks['a'].state == TaskStatus.SKIPPED
    assert tasks['b'].state == TaskStatus.FAILED
    assert tasks['c'].state == TaskStatus.FAILED

    assert tasks['b'].error.get_error_msg() == "type-error"
    assert tasks['c'].error.get_error_msg() == "value-error"

    assert issubclass(tasks['b'].error.get_error_type(), TypeError)
    assert issubclass(tasks['c'].error.get_error_type(), ValueError)