Task Orchestrator
================

Task Orchestrator is a **Python library** for defining and executing
**dependency-aware workflows**. It enables developers to automate
complex task pipelines declaratively using Python decorators, while
handling execution order, failures, and task state management
automatically.

Features
--------

- Define tasks using the ``@Task`` decorator
- Automatic execution order based on task dependencies
- Shared execution context for task outputs
- Task state tracking: ``PENDING``, ``SUCCESS``, ``FAILED``, ``SKIPPED``
- Task tagging and tag-based execution
- Logical task grouping
- Fail-fast handling for dependent tasks
- Conditional task execution using lambdas and built-in helpers
- Retry policies for failed tasks
- Priority-based task execution
- Automatic HTML report generation

How It Works
------------

You define Python functions as tasks using the ``@Task`` decorator.
The engine automatically:

1. Resolves task dependencies and determines execution order
2. Passes outputs from one task to its dependent tasks
3. Tracks execution states (``SUCCESS``, ``FAILED``, ``SKIPPED``)
4. Handles failures and optionally retries tasks based on configuration

Example
-------

Below is a minimal example demonstrating dependency-aware execution:

.. code-block:: python

   from task_engine.core.task import Task
   from task_engine.core.executor import TaskExecutor

   @Task(name="fetch_data")
   def fetch_data():
       """Fetch initial data."""
       return 42

   @Task(name="process_data", depends_on=["fetch_data"])
   def process_data(data):
       """Process data returned by fetch_data."""
       return data * 2

   @Task(name="print_result", depends_on=["process_data"])
   def print_result(result):
       """Print the final result."""
       print(f"Final Result: {result}")

   # Execute all tasks in the correct order
   TaskExecutor.execute()

Expected Output
---------------

.. code-block:: text

   Final Result: 84

.. toctree::
   :maxdepth: 1

   installation

.. toctree::
   :maxdepth: 1

   quickstart


.. toctree::
   :maxdepth: 1

   documentation/index

.. toctree::
   :maxdepth: 1

   cli
