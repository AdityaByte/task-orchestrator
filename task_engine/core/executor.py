from task_engine.core.registry import Registry
from task_engine.core.task import Task
from task_engine.enums.task_status import TaskStatus
from task_engine.exception.task_failed_exception import TaskFailedException

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

        if task.state in [TaskStatus.SUCCESS, TaskStatus.FAILED, TaskStatus.SKIPPED]:
            return

        for dep in task.depends_on:
            try:
                cls._execute_helper(Registry.get_task()[dep])
            except TaskFailedException:
                pass

        if any(Registry.get_task()[dep].state in [TaskStatus.FAILED, TaskStatus.SKIPPED] for dep in task.depends_on):
            task.state = TaskStatus.SKIPPED
            return

        try:
            task.function_ref(*task.function_args, **task.function_kwargs)
            task.state = TaskStatus.SUCCESS
        except Exception as e:
            task.state = TaskStatus.FAILED
            raise TaskFailedException(f"task: {task.name} failed by {e}")