Task Dependencies
===================

In many workflows, tasks depend on the results of other tasks.
**Task Orchestrator** allows you to define dependencies easily
using the ``depends_on`` attribute.

This ensures that tasks are executed in the correct order and
prevents errors caused by missing prerequisites.

---

Defining Dependencies
-----------------------

You can specify dependencies as a list of task names when
defining a task:

.. code-block:: python

   from pravaha.core.task import Task
   from pravaha.core.executor import TaskExecutor

   @Task(name="task1", depends_on=["task2"])
   def task1():
       print("Task1 executed")

   @Task(name="task2")
   def task2():
       print("Task2 executed")

   if __name__ == "__main__":
       TaskExecutor.execute()

Expected Output
-----------------

.. code-block:: text

   Task2 executed
   Task1 executed

---

Notes
-------

- **Task registration order does not matter** when dependencies are defined.
- The executor automatically determines the **correct execution order** based on the dependency graph.
- Circular dependencies will result in an error. Make sure your workflow graph is **acyclic**.
