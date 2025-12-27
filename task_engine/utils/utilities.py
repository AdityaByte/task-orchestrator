"""This file contains helper functions."""
from task_engine.core.task import Task
from operator import attrgetter

def sort_task_on_the_basis_of_priority(tasks: list[Task], reverse=False) -> list[Task]:
    """Returns a sorted task list on the basis of priority order and when reverse is true return in this order
    LOW < NORMAL < HIGH means lowest priority task is executed first.
    Addionally it sorts the tasks in-memory."""
    return sorted(tasks, key=lambda task: task.priority.value, reverse=reverse)

