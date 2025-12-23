import pytest

from task_engine.core.registry import Registry
from task_engine.core.task import Task

@pytest.fixture(scope="function", autouse=True)
def registry_cleanup():
    Registry.tasks = {} # Clean up done.