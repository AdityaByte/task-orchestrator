from task_engine.core.registry import Registry
from task_engine.core.task import Task
from task_engine.enums.task_status import TaskStatus
from task_engine.exception.task_failed_error import TaskFailedError
from task_engine.validation.dag import DAGValidator
from task_engine.context.condition.context import ConditionContext
from datetime import datetime
from time import time, sleep
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

        # Executing task along with checking for retry.
        # Implementing retry logic.
        attempt = 1
        policy = task.retries

        while True:
            try:
                t1 = time()
                task.start_time = datetime.now().strftime("%#I:%M:%S %p")

                try:
                    output = task.function_ref(*inputs)
                except TypeError:
                    output = task.function_ref()

                if output is not None:
                    cls.ExecutionContext[task.name] = output

                task.end_time = datetime.now().strftime("%#I:%M:%S %p")
                task.duration = time() - t1
                task.state = TaskStatus.SUCCESS
                break

            except Exception as e:
                # No retry policy fail immediately.
                if not policy:
                    task.state = TaskStatus.FAILED
                    task.end_time = datetime.now().strftime("%#I:%M:%S %p")
                    task.error = ErrorInformation(e)
                    break

                # If the retry policy exist then we have to check does we have to retry or not.
                if not policy.should_retry(e, attempt):
                    task.state = TaskStatus.FAILED
                    task.end_time = datetime.now().strftime("%#I:%M:%S %p")
                    task.error = ErrorInformation(e)
                    break

                delay = policy.get_delay(attempt)
                print(f"[RETRY] {task.name} attempt {attempt}, retrying in {delay}s")

                attempt += 1
                sleep(delay)


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


    @classmethod
    def dryrun(cls):

        visited_task = set()
        tasks = Registry.get_task()
        for task in tasks:
            cls._dryrun_helper(task, visited_task)

    @classmethod
    def _dryrun_helper(cls, task: Task, order_list: list, visited_task: set):
        order_list = []
        if any(task.name for task in visited_task):
            return
        visited_task.add(task.name)
        order_list.append(task.name)
        for dep_name in task.depends_on:
            pass

"""
task4, task1 -> task2->task3

-> Processed tasks - set()
-> list of string.
"""