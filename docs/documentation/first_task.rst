Creating Your First Workflow
============================

A workflow is a collection of tasks executed together by the engine.
Each task represents a unit of work, and workflows allow these tasks
to be executed in a controlled and predictable order.

In this guide, you will create a simple workflow with two tasks to
understand how task execution and shared execution context work.

Example Scenario
----------------

We will create:

- One task that increments a shared counter
- Another task that prints the updated counter value

This example demonstrates **task registration order** and **shared
execution context** using a mutable object.

.. code-block:: python

   from task_engine.core.task import Task
   from task_engine.core.executor import TaskExecutor

   # Shared execution context
   counter = {"value": 0}

   @Task(name="increment")
   def increment():
       counter["value"] += 1

   @Task(name="print_counter_value")
   def print_counter_value():
       print("Counter value is:", counter["value"])

   # Execute all registered tasks
   TaskExecutor.execute()

Expected Output
---------------

.. code-block:: text

   Counter value is: 1

Execution Order
---------------

Tasks are registered in the order they are defined in the source file.
By default, the executor runs tasks **synchronously in registration order**
unless dependencies or execution rules are specified.

In this example:

1. ``increment`` is registered first and executed first
2. ``print_counter_value`` is registered next and executed afterward

.. note::

   This execution order behavior applies only when no explicit
   dependencies are defined. Dependency-based execution is covered
   in the next section.
