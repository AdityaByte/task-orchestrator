from task_engine.core.task import Task
from task_engine.core.executor import TaskExecutor
from task_engine.core.report import analyze

@Task(name="another_func", depends_on=["logger"])
def another_func():
    print("what are you doing")

@Task(name='logger', depends_on=["func"])
def logger():
    raise Exception("hello world")
    print("Logger")

@Task(name="func")
def func():
    print("Hello world")

task = Task(name="func")

if __name__ == "__main__":
    TaskExecutor.execute()
    analyze()