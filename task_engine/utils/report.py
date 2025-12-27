"""
This class mainly handles the report generation.
"""
from task_engine.core.registry import Registry
from task_engine.enums.task_status import TaskStatus

def analyze():
   print("Analyzed result of the tasks:")
   tasks = Registry.get_task()
   for task in tasks.values():
       print(f"Function: {task.name}")
       print(f"\tState: {task.state}")
       print(f"\tStart Time: {task.start_time if task.state is not TaskStatus.SKIPPED else 'Task is skipped'}")
       print(f"\tEnd time: {task.end_time if task.state is not TaskStatus.SKIPPED else 'Task is skipped' }")
       print(f"\tDuration: {task.duration}")
       print(f"\tError: {task.error if not '' else 'No error'}")
       print("*" * 20)