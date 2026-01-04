Conditional-Based Task Execution
====================================

Task Orchestrator allows tasks to execute **conditionally** based on:

1. Previous task results: ``SUCCESS``, ``FAILED``, or ``SKIPPED``
2. User-defined conditions (lambda functions)
3. Environment variables
4. Exceptions raised by tasks

This provides fine-grained control over workflow execution.

---

Executing Tasks Based on Previous Task Results
-------------------------------------------------

You can trigger tasks based on the success or failure of other tasks:

.. code-block:: python

   from pravaha.core.task import Task
   from pravaha.context.condition.builders import OnFailure, OnSuccess
   from pravaha.core.executor import TaskExecutor

   @Task(name="a")
   def a():
       print("a executed")

   @Task(name="b", condition=OnSuccess("a"))
   def b():
       print("b executed")

   @Task(name="c", condition=OnFailure("a"))
   def c():
       print("c executed")

   # OnSkipped() is also available for tasks skipped due to dependencies

   if __name__ == "__main__":
       TaskExecutor.execute()

Expected Output
------------------

.. code-block:: text

   a executed
   b executed

---

Executing Tasks Based on Environment Variables
------------------------------------------------

Tasks can execute only if certain environment conditions are met:

.. code-block:: python

   from pravaha.core.task import Task
   from pravaha.context.condition.builders import Env
   from pravaha.core.executor import TaskExecutor

   # Execute this task only when environment is set to "prod"
   @Task(name="deploy", condition=Env("prod"))
   def deploy():
       print("Deploying to production environment")

   TaskExecutor.execute()

---

Executing Tasks Using User-Defined Conditions
------------------------------------------------

You can pass a lambda function that receives the **execution context**:

.. code-block:: python

   from pravaha.core.task import Task
   from pravaha.core.executor import TaskExecutor

   @Task(name="check_condition", condition=lambda ctx: 10 > 9)
   def check_condition():
       print("Yes, 10 is greater than 9")

   TaskExecutor.execute()

Expected Output
-----------------

.. code-block:: text

   Yes, 10 is greater than 9

---

Executing Tasks on Exceptions
--------------------------------

Trigger tasks when specific exceptions occur in other tasks:

.. code-block:: python

   from pravaha.core.task import Task
   from pravaha.context.condition.builders import OnExceptionType
   from pravaha.core.executor import TaskExecutor

   @Task(name="a")
   def a():
       raise ValueError("Value error")  # Simulate an exception

   # Execute only if "a" raises a ValueError
   @Task(name="handle_error", condition=OnExceptionType("a", ValueError))
   def handle_error():
       print("Handling ValueError from task 'a'")

   TaskExecutor.execute()

Expected Output
-----------------

.. code-block:: text

   Handling ValueError from task 'a'
