Pravaha
============================

Pravaha (a sanskrit word which means flow) is a **Python library** for defining and executing
**dependency-aware workflows**, allowing developers
to automate complex workflows declaratively using Python decorators.

Features
--------

- Define tasks using the ``@Task`` decorator
- Automatic execution order based on task dependencies
- Built-in logging and execution context for task outputs
- Task states tracking: ``PENDING``, ``SUCCESS``, ``FAILED``, ``SKIPPED``
- Fail-fast error handling for dependent tasks
- Lightweight and extensible for workflow automation
- Conditional Task Execution on the basis of environment variables, previous task output and success failure of previous task.
- Retry Policy
- Task Output Sharing
- Priority Based Task Execution
- Tagging of tasks
- Task Group Execution
- HTML Report Generation

How It Works
------------

You define functions as tasks using the ``@Task`` decorator. The engine
automatically:

1. Resolves task dependencies and enforces execution order
2. Passes outputs from one task to dependent tasks
3. Tracks execution states (``SUCCESS``, ``FAILED``, ``SKIPPED``)
4. Handles errors and optionally retries failed tasks (planned feature)

Example
-------

.. code-block:: python

    from pravaha.core.task import Task
    from pravaha.core.executor import TaskExecutor

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

.. code-block::

    Final Result: 84

Local Setup
-----------

Since the library is not yet published, you can set it up locally:

1. Clone the repository:

   .. code-block:: bash

       git clone <repository-url>
       cd task-orchestrator

2. Install development dependencies:

   .. code-block:: bash

       pip install -e .[dev]

Running Tests
-------------

The library includes **unit tests** for all core components:

- Task decorator
- Registry
- Executor logic

Run the tests:

.. code-block:: bash

    pytest

Notes:

- Tests reset global state to avoid cross-test contamination
- DAG validation and dependency execution are fully covered
- CI/CD workflows can run tests automatically on every commit

Contributing
------------

Contributions are welcome! Please follow these guidelines:

- Follow existing code style and naming conventions
- Add unit tests for new features or bug fixes
- Keep commits focused and descriptive (use conventional commits)
- Ensure tests pass before submitting a pull request
