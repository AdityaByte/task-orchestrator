Quickstart
==========

This guide shows how to create and run your first workflow using
**Task Orchestrator**.

Create Your First Task
----------------------

Import the ``@Task`` decorator and define a task as a normal Python
function:

.. code-block:: python

   from task_engine.core.task import Task
   from task_engine.core.executor import TaskExecutor

   @Task(name="task1")
   def task1():
       print("Hello from Task Orchestrator")

Run the Workflow
----------------

Execute all registered tasks using the executor:

.. code-block:: python

   if __name__ == "__main__":
       TaskExecutor.execute()

Expected Output
---------------

.. code-block:: text

   Hello from Task Orchestrator
