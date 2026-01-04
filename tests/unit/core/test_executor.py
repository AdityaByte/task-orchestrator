from pravaha.core.executor import TaskExecutor
from pravaha.core.task import Task
from pravaha.core.registry import Registry
from pravaha.enums.task_status import TaskStatus
from pravaha.context.condition.builders import OnFailed
from pravaha.retry.policy import RetryPolicy
from pravaha.retry.backoff import fixed_delay
from pravaha.enums.task_priority import TaskPriority

def test_single_task_execution_success():

    @Task(name="task")
    def task():
        return "Task is completed"

    TaskExecutor.execute()

    tasks = Registry.get_task()
    assert tasks["task"].state == TaskStatus.SUCCESS

    assert TaskExecutor.ExecutionContext.get("task") == "Task is completed"

def test_task_with_dependencies_execute_in_order():

    execution_order = []

    @Task(name="task1", depends_on=["task2"])
    def task1(name):
        execution_order.append("task1")
        return f"Hi I am {name}"

    @Task(name="task2")
    def task2():
        execution_order.append("task2")
        return "aditya"

    TaskExecutor.execute()
    assert execution_order == ["task2", "task1"]

    assert TaskExecutor.ExecutionContext.get("task1") == "Hi I am aditya"

def test_task_skipped_when_dependency_failed():

    @Task(name="task1", depends_on=["task2"])
    def task1():
        pass

    @Task(name="task2")
    def task2():
        raise Exception("Something went wrong")

    TaskExecutor.execute()

    assert Registry.get_task().get("task1").state == TaskStatus.SKIPPED
    assert Registry.get_task().get("task2").state == TaskStatus.FAILED

def test_task_skipped_when_condition_false():

    @Task(name="task", condition= lambda ctx: False)
    def task():
        pass

    TaskExecutor.execute()

    assert Registry.get_task().get("task").state == TaskStatus.SKIPPED

def test_condition_based_on_previous_task_status():

    is_task1_executed = {"value": False}

    @Task(name="task2")
    def task2():
        raise Exception("boom")

    @Task(name="task1", condition=OnFailed("task2"))
    def task1():
        is_task1_executed['value'] = True
        print("Task2 failed")

    TaskExecutor.execute()

    assert Registry.get_task().get("task2").state == TaskStatus.FAILED
    assert is_task1_executed['value'] == True

def test_retry_policy_eventual_success():

    counter = {"value": 0}

    @Task("task1", depends_on=['task2'])
    def task1():
        print("Task1 executed")

    @Task("task2", retries=RetryPolicy(max_retries=3, retry_on=(ValueError, ), backoff=fixed_delay(0.1)))
    def task2():
        if counter['value'] == 2:
            print("Task2 executed")
            return
        counter['value'] += 1
        raise ValueError("value error")

    TaskExecutor.execute()

    assert Registry.get_task().get("task1").state == TaskStatus.SUCCESS
    assert Registry.get_task().get("task2").state == TaskStatus.SUCCESS

def test_retry_policy_exhausted_failure():

    @Task("task1", depends_on=["task2"])
    def task1():
        print("task1 executed")

    @Task("task2", retries=RetryPolicy(max_retries=3, retry_on=(ValueError,), backoff=fixed_delay(0.1)))
    def task2():
        raise ValueError("Value error")

    TaskExecutor.execute()

    assert Registry.get_task().get("task1").state == TaskStatus.SKIPPED
    task = Registry.get_task().get("task2")
    assert task.state == TaskStatus.FAILED
    assert isinstance(task.error.exception, ValueError)

def test_execute_only_tagged_task():

    executed_task = {"value": None}

    @Task("task1", tag="dev")
    def task1():
        executed_task['value'] = "dev"

    @Task("task2", tag="prod")
    def task2():
        executed_task['value'] = "prod"

    TaskExecutor.execute(tags=("dev", ))

    assert executed_task['value'] == "dev"
    assert Registry.get_task().get("task2").state == TaskStatus.PENDING

def test_taskgroup_executes_dependencies():

    @Task("task1", depends_on=["task2"])
    def task1():
        pass

    @Task("task2")
    def task2():
        pass

    @Task("task3")
    def task3():
        pass

    # Making a task group of only one task - task1 since it depends on the task2.
    # So the task2 also executes but the task3 won't executed.

    TaskExecutor.execute(taskgroup=("task1", ))

    tasks = Registry.get_task()
    assert tasks['task1'].state == TaskStatus.SUCCESS
    assert tasks['task2'].state == TaskStatus.SUCCESS
    assert tasks['task3'].state == TaskStatus.PENDING

def test_priority_execution_order():

    execution_order = []

    @Task("task1", priority=TaskPriority.HIGH)
    def task1():
        execution_order.append("task1")

    @Task("task2", priority=TaskPriority.LOW)
    def task2():
        execution_order.append("task2")

    @Task("task3", priority=TaskPriority.NORMAL)
    def task3():
        execution_order.append("task3")

    TaskExecutor.execute()

    assert execution_order == ['task1', 'task3', 'task2']
