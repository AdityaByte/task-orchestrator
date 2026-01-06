from pravaha.core.registry import Registry
from pravaha.exception.task import TaskNotFoundError
from pravaha.core.task import Task

"""
Using Depth first traversal algorithm.
How we are resolving dependencies?

Function Parameter: Takes a tuple of task names.
Returns Dictionary

Step 1: Fetching all the task from the task registry.
Step 2: Making a data-type for resolved tasks.
Step 3: Making a data-type for visited tasks.
Step 4: Creating a dfs function.
-> Takes task-name as argument.
-> Checking the task is visited if it do then we simply returns.
-> Checking the task exists in the registry or not if not we raise an exception.
-> Now resolving the dependency because it is a depth first search algo.
-> So we are putting each and every task to the resolved dictionary.

Step 5: Calling the dfs function for each task.
Step 6: Returning the resolved dictionary.

"""

def resolve_dependencies(selected_tasks: tuple[str]) -> dict[str, Task]:
    registry = Registry.get_task()  # {name: Task}
    resolved: dict[str, Task] = {}
    visited: set[str] = set()

    def dfs(task_name: str):
        if task_name in visited:
            return

        if task_name not in registry:
            raise TaskNotFoundError(
                f"Task with name '{task_name}' does not exist in registry"
            )

        visited.add(task_name)
        task: Task = registry[task_name]

        for dep_name in task.depends_on.dependencies:
            dfs(dep_name)

        resolved[task_name] = task # Adding resolved task to dictionary.

    for task_name in selected_tasks:
        dfs(task_name)

    return resolved
