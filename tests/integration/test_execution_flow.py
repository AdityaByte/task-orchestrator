from pravaha.core.task import Task
from pravaha.core.registry import Registry
from pravaha.enums.task_status import TaskStatus
from pravaha.core.executor import TaskExecutor
import pytest


def test_execute_simple_linear_workflow_and_context_passes_correctly():
    """There were three tasks a, b and c and the task is dependent in this order
    a->b->c so the output of each tasks are correctly transferred to other tasks."""

    exec_order: list[str] = []

    @Task("a", depends_on=['b'])
    def a(data: str) -> None:
        exec_order.append("a")
        print("a", data, sep="")

    @Task("b", depends_on=['c'])
    def b(data: str) -> str:
        exec_order.append("b")
        return "b" + data

    @Task("c")
    def c() -> str:
        exec_order.append("c")
        return "c"

    TaskExecutor.execute()

    tasks = Registry.get_task()

    assert exec_order == ['c', 'b', 'a']
    assert tasks['a'].state == TaskStatus.SUCCESS
    assert tasks['b'].state == TaskStatus.SUCCESS
    assert  tasks['c'].state == TaskStatus.SUCCESS

    exec_ctx = TaskExecutor.ExecutionContext

    assert exec_ctx['c'] == 'c'
    assert exec_ctx['b'] == 'bc'
    with pytest.raises(KeyError):
        assert exec_ctx['a'] is None

def test_execute_workflow_with_shared_dependencies():
    """
    b -> a and c -> a
    a is the shared dependency so check a will be executed only once. No
    duplicate execution may occur.
    """

    exec_count = {"a": 0, "b": 0, "c": 0}

    @Task("a")
    def a():
        exec_count['a'] += 1
        pass

    @Task("b", depends_on=['a'])
    def b():
        exec_count['b'] += 1
        pass

    @Task("c", depends_on=['a'])
    def c():
        exec_count['c'] += 1
        pass

    TaskExecutor.execute()

    assert exec_count['a'] == 1
    assert exec_count['b'] == 1
    assert exec_count['c'] == 1

