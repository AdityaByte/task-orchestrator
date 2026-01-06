"""
This file tests Task initialization behavior.
"""
from pravaha.core.task import Task
from pravaha.enums.task_status import TaskStatus
from pravaha.dependency.dependency import Dependency
import pytest

def test_task_initializes_with_required_name():
    task = Task(name="demo_task")
    assert task.name == "demo_task"

def test_task_defaults_when_optional_args_not_provided():
    task = Task(name="demo_task")
    assert isinstance(task.depends_on, Dependency)
    assert task.state == TaskStatus.PENDING
    assert task.error is None
    assert task.start_time == ""
    assert task.end_time == ""
    assert task.duration is None
    assert task.retries is None
    assert task.function_ref is None

def test_task_accepts_dependency_list():
    task = Task("demo_task", depends_on=['task1', 'task2'])
    dependency_set = set(['task1', 'task2'])
    assert dependency_set == set(task.depends_on.dependencies)

def test_task_does_not_share_depends_on_between_instances():
    task1 = Task('task1', depends_on=['task3'])
    task2 = Task('task2', depends_on=['task3'])

    assert task1.depends_on is not task2.depends_on

def test_task_raises_type_error_on_invalid_depends_on_argument():

    with pytest.raises(TypeError):
        task1 = Task("task1", depends_on=tuple())