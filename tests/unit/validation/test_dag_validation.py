from task_engine.core.registry import Registry
from task_engine.core.task import Task
from task_engine.validation.dag import DAGValidator
from task_engine.exception.validation import MissingDependencyError, CircularDependencyError
import pytest

def test_valid_linear_dag():
    @Task("a", depends_on=['b'])
    def a():
        pass
    @Task("b", depends_on=['c'])
    def b():
        pass
    @Task("c")
    def c():
        pass

    tasks = Registry.get_task()
    assert DAGValidator.validate(tasks) is True

def test_valid_branching_dag():
    @Task("a", depends_on=['b', 'c'])
    def a():
        pass
    @Task("b")
    def b():
        pass
    @Task("c")
    def c():
        pass

    tasks = Registry.get_task()
    assert DAGValidator.validate(tasks) is True

def test_dag_raises_missing_dependency_error():

    @Task("a", depends_on=['b'])
    def a():
        pass

    tasks = Registry.get_task()

    with pytest.raises(MissingDependencyError):
        DAGValidator.validate(tasks)

def test_dag_raises_missing_dependency_error_on_deep_graph():

    @Task("a")
    def a():
        pass
    @Task("b", depends_on=['a'])
    def b():
        pass
    @Task("c", depends_on=['d']) # d doesn't exists.
    def c():
        pass

    tasks = Registry.get_task()

    with pytest.raises(MissingDependencyError):
        DAGValidator.validate(tasks)

def test_simple_cycle():
    @Task("a", depends_on=['b'])
    def a():
        pass
    @Task("b", depends_on=['a'])
    def b():
        pass

    tasks = Registry.get_task()

    with pytest.raises(CircularDependencyError):
        DAGValidator.validate(tasks)

def test_self_dependency_cycle():
    @Task("a", depends_on=['a'])
    def a():
        pass

    tasks = Registry.get_task()

    with pytest.raises(CircularDependencyError):
        DAGValidator.validate(tasks)

def test_long_cycle():
    @Task("a", depends_on=['b'])
    def a():
        pass
    @Task("b", depends_on=['c'])
    def b():
        pass
    @Task("c", depends_on=['d'])
    def c():
        pass
    @Task("d", depends_on=['e'])
    def d():
        pass
    @Task("e", depends_on=['a'])
    def e():
        pass

    tasks = Registry.get_task()
    with pytest.raises(CircularDependencyError):
        DAGValidator.validate(tasks)

def test_disconnected_graph():
    @Task("a")
    def a():
        pass
    @Task("b")
    def b():
        pass
    @Task("c")
    def c():
        pass
    @Task("d", depends_on=['c'])
    def d():
        pass

    tasks = Registry.get_task()
    DAGValidator.validate(tasks) is True