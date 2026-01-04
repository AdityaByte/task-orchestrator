from pravaha.core.task import Task
from pravaha.core.executor import TaskExecutor
from pravaha.report.report import generate_report
import time


@Task(name="task1", depends_on=['task2'])
def task1():
    time.sleep(4)
    print("Hello world")

@Task("task2")
def task2():
    time.sleep(2)
    print("Task2 executed")
    raise ValueError("Value error raised.")

TaskExecutor.execute()
generate_report("my_workflow")