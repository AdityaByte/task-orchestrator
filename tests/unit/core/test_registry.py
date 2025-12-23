from task_engine.core.registry import Registry
from task_engine.core.task import Task


def test_set_task_registers_new_task():
    task1 = Task("task1")
    Registry.set_task("task1", task1)

    assert Registry.tasks["task1"] is not None

def test_set_task_does_not_override_existing_task():
    """
    task1 has a different dependency and creating another task with same name
    So the old task won't be overrides.
    :return:
    """
    task1 = Task("task1")
    Registry.set_task("x", task1)

    task2 = Task("task2")
    Registry.set_task("x", task2)

    # Checking the name attribute of the task for confirming they won't be overridden.
    assert Registry.tasks["x"].name == "task1"

def test_get_task_returns_all_registered_tasks():
    """
    Saving 4 tasks and at last checking the length and the tasks.
    :return:
    """
    for i in range(4):
        new_task = Task(f"task{i+1}")
        Registry.set_task(f"task{i+1}", new_task)

    tasks = Registry.get_task()
    assert len(tasks) == 4
    for task in tasks:
        assert task in ["task1", "task2", "task3", "task4"]

def test_get_task_returns_empty_dict_when_no_tasks_registered():
    tasks = Registry.get_task()
    assert tasks == {}

def test_registry_stores_tasks_by_name_key():
    task1 = Task("task1")
    Registry.set_task(task1.name, task1)
    assert "task1" in Registry.get_task().keys()

def test_registry_is_class_level_shared_state():
    registry = Registry()
    registry.set_task("task1", Task("task1"))

    another_registry = Registry()
    assert another_registry.get_task()["task1"] is not None

def test_set_task_accepts_task_object_reference():
    task1 = Task("task1")
    Registry.set_task("task1", task1)

    task2 = Task("task2")

    assert Registry.get_task()["task1"] is task1
    assert Registry.get_task()["task1"] is not task2

def test_registry_persists_tasks_across_calls():
    assert Registry.get_task() == {}
    Registry.set_task("task1", Task("task1"))
    assert len(Registry.get_task()) == 1
    Registry.tasks = {}
    assert len(Registry.get_task()) == 0

def test_registry_can_be_manually_cleared_for_test_isolation():
    Registry.set_task("task1", Task("task1"))
    assert Registry.get_task() is not None
    Registry.tasks = {}
    assert Registry.get_task() == {}