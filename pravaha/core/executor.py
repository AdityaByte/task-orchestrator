from pravaha.core.registry import Registry
from pravaha.core.task import Task
from pravaha.enums.task_status import TaskStatus
from pravaha.validation.dag import DAGValidator
from pravaha.context.condition.context import ConditionContext
from datetime import datetime
from time import time, sleep
import os
from pravaha.core.task import ErrorInformation
from pravaha.utils.utilities import sort_task_on_the_basis_of_priority, filter_tasks_on_the_basis_of_tags
from pravaha.utils.dep_resolver import resolve_dependencies

class TaskExecutor:
    """
    This class has all the methods for executing the task.
    """
    ExecutionContext: dict = {}
    tasks: dict = {}

    @classmethod
    def execute(cls, tags: tuple = (), taskgroup: tuple= ()):
        """
        Task is executed through this method.
        Args:
            tags (tuple): Tuple of tags.
            taskgroup (tuple): Task group.
        Returns:
            None
        """
        cls.tasks = Registry.get_task()

        # Validating the dag graph.
        DAGValidator.validate(cls.tasks)

        # If tags is not empty then executing only tags tasks.
        if tags:
            cls.tasks = filter_tasks_on_the_basis_of_tags(cls.tasks.values(), set(tags))

        if taskgroup:
            cls.tasks = resolve_dependencies(taskgroup)

        # Sorting tasks on the basis of priority.
        cls.tasks = sort_task_on_the_basis_of_priority(cls.tasks.values())

        # The above sorted funs directly sending the list of values.
        for task in cls.tasks.values():
            cls._execute_helper(task)


    @classmethod
    def _execute_helper(cls, task: Task):

        if task.state in [TaskStatus.SUCCESS, TaskStatus.FAILED, TaskStatus.SKIPPED]:
            return

        for dep_name in task.depends_on:
            dep_task = cls.tasks[dep_name]
            cls._execute_helper(dep_task)

        if any(cls.tasks[dep].state in [TaskStatus.FAILED, TaskStatus.SKIPPED] for dep in task.depends_on):
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
            task_states={name: t.state for name, t in cls.tasks.items()},
            execution_context=cls.ExecutionContext,
            task_errors={name: t.error for name, t in cls.tasks.items()}
        )

        return bool(task.condition(ctx))


"""
task4, task1 -> task2->task3

-> Processed tasks - set()
-> list of string.
"""