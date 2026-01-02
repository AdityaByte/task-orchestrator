Command Line Utility
========================

Task Orchestrator provides a **command-line utility** that allows you to:

- Run task files or modules
- Execute tasks selectively by tag or task group
- Generate HTML reports for workflows

You can view available commands and flags using:

.. code-block:: bash

   task-engine -h

---

Running a Task File
-----------------------

To run a Python file containing tasks:

.. code-block:: bash

   task-engine run --file filename.py --tags <tag1,tag2> --taskgroups <group1,group2>

**Parameters:**

- ``--file`` : Path to the Python file containing tasks
- ``--tags`` : (Optional) Execute only tasks with the specified tags
- ``--taskgroups`` : (Optional) Execute only tasks in the specified task groups

---

Running a Module
--------------------

To run tasks defined inside a Python module:

.. code-block:: bash

   task-engine run --module aditya.module

**Parameters:**

- ``--module`` : Module path containing tasks (e.g., ``aditya.module``)

---

Generating Reports
--------------------

You can generate an **HTML report** for your workflow execution:

.. code-block:: bash

   task-engine run --file my-workflow.py --report my-workflow

**Parameters:**

- ``--report`` : Name of the workflow report to generate (the HTML file will be created under ``./reports/``)

---

Notes
-------

- CLI execution respects **task dependencies, priorities, tags, and groups**.
- You can combine **tags**, **task groups**, and **report generation** in a single command.
