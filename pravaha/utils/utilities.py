"""This file contains helper functions."""
from pravaha.core.task import Task
from pravaha.exception.tag import TagNotFoundError

def sort_task_on_the_basis_of_priority(tasks: list[Task], reverse=False) -> dict:
    """Returns a sorted task list on the basis of priority order and when reverse is true return in this order
    LOW < NORMAL < HIGH means lowest priority task is executed first.
    Addionally it sorts the tasks in-memory."""
    sorted_tasks = sorted(tasks, key=lambda task: task.priority.value, reverse=reverse)
    return _return_task_dict(sorted_tasks)


def filter_tasks_on_the_basis_of_tags(tasks: list[Task], tags: set) -> dict:
    """This method filter tasks on the basis of tag if all the tags were exists then we simply returns
    the filtered list otherwise if some tags were missing in that case we raise an exception."""

    tag_tasks = list()
    tag_lookup = set() # It takes care of the tags all the tags that we put must exists if doesn't then we throws an error.
    for task in tasks:
        if task.tag in tags:
            tag_tasks.append(task)
            tag_lookup.add(task.tag)

    is_some_tag_missing = tags - tag_lookup
    if is_some_tag_missing:
        raise TagNotFoundError(f"Missing tag: {is_some_tag_missing}")

    # Returning a list of dictionary.
    return _return_task_dict(tag_tasks)

def _return_task_dict(tasks: list[Task]) -> list[dict]:
    final_dict = {}
    for task in tasks:
        final_dict[task.name] = task

    return final_dict