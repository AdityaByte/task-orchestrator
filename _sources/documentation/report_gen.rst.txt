Report Generation
=================

Task Orchestrator provides built-in **HTML report generation** to help you
analyze workflow executions.

Reports include detailed information such as:

- Task execution order
- Execution duration for each task
- Task status (``SUCCESS``, ``FAILED``, ``SKIPPED``)
- Overall workflow execution summary

This is especially useful for debugging, auditing, and monitoring workflows.

Generating a Report
-------------------

After executing a workflow, you can generate a report using the
``generate_report`` function from the report module.

.. code-block:: python

   import time
   from pravaha.core.task import Task
   from pravaha.core.executor import TaskExecutor
   from pravaha.report.report import generate_report

   @Task(name="a")
   def task_a():
       time.sleep(3)
       print("a executed")

   # Execute the workflow
   TaskExecutor.execute()

   # Generate the HTML report
   generate_report("my-workflow")

Report Output Location
----------------------

The generated report is saved automatically in the following directory:

.. code-block:: text

   ./reports/my-workflow.html

The report directory is created automatically if it does not already exist.

Viewing the Report
------------------

Open the generated ``.html`` file in any web browser to view the full
execution report.
