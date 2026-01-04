import pytest

from pravaha.core.registry import Registry
from pravaha.core.task import Task

@pytest.fixture(scope="function", autouse=True)
def registry_cleanup():
    Registry.tasks = {} # Clean up done.