"""
This class mainly handles the report generation.
"""
from task_engine.core.registry import Registry

def analyze():
   tasks = Registry.get_task()
   for task in tasks.values():
       print(f"Function name: {task.name:<15} | State: {task.state}")