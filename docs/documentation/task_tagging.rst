Task Tagging
============

Task Orchestrator allows you to **tag tasks** to categorize them. This is
useful when you have multiple types of tasks, such as **development**,
**testing**, or **production tasks**, and you want to execute only a subset
based on tags.

---

Defining Tags
-------------

Use the ``tag`` parameter when defining a task:

.. code-block:: python

   from pravaha.core.task import Task
   from pravaha.core.executor import TaskExecutor

   @Task(name="task1", tag="dev")
   def task1():
       print("Dev task executed")

   @Task(name="task2", tag="prod")
   def task2():
       print("Prod task executed")

Executing Tasks by Tag
----------------------

You can execute only tasks with specific tags using the ``tags`` parameter
of the executor:

.. code-block:: python

   if __name__ == "__main__":
       # Execute only tasks tagged with "prod"
       TaskExecutor.execute(tags=("prod",))

Expected Output
---------------

.. code-block:: text

   Prod task executed

---

Notes
-----

- When a tagged task depends on another task (tagged or untagged),
  the executor **automatically includes all dependencies** in the execution plan.
- This ensures that dependencies are **never skipped**, even if they have a different tag.
- Tags allow selective execution without modifying the workflow code.
