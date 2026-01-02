Task Priority
=============

Task Orchestrator allows you to assign **priority levels** to tasks.
Tasks with higher priority are executed before tasks with lower priority.
You can also reverse the execution order if needed.

---

Defining Task Priority
---------------------

Use the ``priority`` parameter when defining a task:

.. code-block:: python

   from task_engine.core.task import Task
   from task_engine.enums.task_priority import TaskPriority
   from task_engine.core.executor import TaskExecutor

   @Task(name="task1", priority=TaskPriority.HIGH)
   def task1():
       print("Task1 executed")

   @Task(name="task2", priority=TaskPriority.LOW)
   def task2():
       print("Task2 executed")

   @Task(name="task3", priority=TaskPriority.NORMAL)
   def task3():
       print("Task3 executed")

   if __name__ == "__main__":
       TaskExecutor.execute()

Expected Output
---------------

.. code-block:: text

   Task1 executed
   Task3 executed
   Task2 executed

---

Notes
-----

- Default execution is **HIGH → NORMAL → LOW**.
- The executor supports a **reverse flag** if you want to run low-priority tasks first.
- Priority is evaluated **after dependency resolution**, so tasks are still executed
  in an order that respects both **dependencies** and **priority**.
- Useful when multiple independent tasks exist, and some must run earlier.
