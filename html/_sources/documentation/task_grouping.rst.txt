Task Grouping
=============

In large workflows, you may want to execute only a **subset of tasks** for
debugging, testing, or partial runs. Task Orchestrator allows you to
group tasks and execute only the selected group.

---

Example: Executing a Group of Tasks
-----------------------------------

.. code-block:: python

   from task_engine.core.task import Task
   from task_engine.core.executor import TaskExecutor

   @Task(name="a")
   def a():
       print("a")

   @Task(name="b")
   def b():
       print("b")

   @Task(name="c")
   def c():
       print("c")

   if __name__ == "__main__":
       # Execute only tasks "a" and "c"
       TaskExecutor.execute(taskgroup=("a", "c"))

Expected Output
---------------

.. code-block:: text

   a
   c

---

Notes
-----

- The `taskgroup` parameter takes a **tuple of task names**.
- Only the tasks in the group are executed; others are skipped.
- Task dependencies are still respected. If a task in the group depends on
  other tasks not in the group, those dependencies may also be executed automatically.
- This feature is helpful for **debugging**, testing, or running partial workflows.
