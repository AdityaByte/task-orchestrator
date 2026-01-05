from pravaha.core.task import Task
from pravaha.core.executor import TaskExecutor
from pravaha.enums.task_status import TaskStatus
from pravaha.core.registry import Registry
from pravaha.exception.task import TaskNotFoundError
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

