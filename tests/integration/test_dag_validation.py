from pravaha.core.task import Task
from pravaha.core.executor import TaskExecutor
from pravaha.exception.validation import MissingDependencyError, CircularDependencyError
from pravaha.core.registry import Registry
from pravaha.enums.task_status import TaskStatus
import pytest

def test_missing_dependency_raises_error():

    @Task("a", depends_on=['b']) # But b won't exist.
    def a():
        pass

    with pytest.raises(MissingDependencyError):
        TaskExecutor.execute()

def test_simple_circular_dependency_detected():

    @Task("a", depends_on=['b'])
    def a():
        pass

    @Task("b", depends_on=['a'])
    def b():
        pass

    with pytest.raises(CircularDependencyError):
        TaskExecutor.execute()

def test_disconnected_dag_but_valid():

    @Task("a", depends_on=['b'])
    def a():
        pass

    @Task("b")
    def b():
        pass

    @Task("c", depends_on=['a'])
    def c():
        pass

    @Task("d")
    def d():
        pass

    TaskExecutor.execute()

    tasks = Registry.get_task().values()

    assert len(tasks) == 4

    for task in tasks:
        task.state == TaskStatus.SUCCESS