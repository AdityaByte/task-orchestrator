from task_engine.core.registry import Registry
from task_engine.core.task import Task

class TaskExecutor:
    """
    Don't need any instance for calling this method.
    """
    tasks: {} = None

    @classmethod
    def execute(cls):
        tasks = Registry.get_task()
        for task in tasks.values():
            cls._execute_helper(task)

    @classmethod
    def _execute_helper(cls, task: Task):

        if task.executed:
            return

        for dep in task.depends_on:
            cls._execute_helper(Registry.get_task()[dep])

        task.function_ref(*task.function_args, **task.function_kwargs)
        task.executed = True