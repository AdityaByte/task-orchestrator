from task_engine.core.task import Task
from task_engine.core.executor import TaskExecutor

@Task(name="another_func", depends_on=["logger"])
def another_func():
    print("what are you doing")

@Task(name='logger', depends_on=["func"])
def logger():
    print("Logger")

@Task(name="func")
def func():
    print("Hello world")

if __name__ == "__main__":
    TaskExecutor.execute()