from task_engine.core.registry import Registry
from task_engine.core.task import Task
from task_engine.enums.task_status import TaskStatus
from task_engine.exception.task_failed_error import TaskFailedError
from task_engine.validation.dag import DAGValidator
from task_engine.context.condition.context import ConditionContext
from datetime import datetime
from time import time
import os
from task_engine.core.task import ErrorInformation

class TaskExecutor:
    """
    Don't need any instance for calling this method.
    """
    ExecutionContext: dict = {}


    @classmethod
    def execute(cls):
        tasks = Registry.get_task()
        DAGValidator.validate(tasks)

        for task in tasks.values():
            cls._execute_helper(task)


    @classmethod
    def _execute_helper(cls, task: Task):

        if task.state in [TaskStatus.SUCCESS, TaskStatus.FAILED, TaskStatus.SKIPPED]:
            return

        try:
            for dep_name in task.depends_on:
                dep_task = Registry.get_task()[dep_name]
                cls._execute_helper(dep_task)

            if any(Registry.get_task()[dep].state in [TaskStatus.FAILED, TaskStatus.SKIPPED] for dep in task.depends_on):
                task.state = TaskStatus.SKIPPED
                return

            # Checking for condition if any condition exists and the result of that condition
            # concluded to false then we skip that case.
            if not cls._evaluate_condition(task):
                task.state = TaskStatus.SKIPPED
                return

            # Preparing inputs for dependency outputs.
            inputs = [cls.ExecutionContext.get(dep_name) for dep_name in task.depends_on]

            # Executing task
            try:
                t1 = time()
                task.start_time = datetime.now().strftime("%#I:%M:%S %p")
                output = task.function_ref(*inputs)
            except TypeError:
                output = task.function_ref()

            if output is not None:
                cls.ExecutionContext[task.name] = output
            task.end_time = datetime.now().strftime("%#I:%M:%S %p")
            task.duration = time() - t1
            task.state = TaskStatus.SUCCESS

        except Exception as e:
            task.state = TaskStatus.FAILED
            task.end_time = datetime.now().strftime("%#I:%M:%S %p")
            task.error = ErrorInformation(e)


    @classmethod
    def _evaluate_condition(cls, task: Task):
        if task.condition is None:
            return True

        ctx = ConditionContext(
            env=os.environ,
            task_states={name: t.state for name, t in Registry.get_task().items()},
            execution_context=cls.ExecutionContext,
            task_errors={name: t.error for name, t in Registry.get_task().items()}
        )

        return bool(task.condition(ctx))