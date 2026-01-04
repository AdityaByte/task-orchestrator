from pravaha.core.registry import Registry
from importlib.resources import files
from pravaha.core.task import Task
from datetime import datetime
from pathlib import Path


def generate_report(workflow_name: str):
    """Generates HTML report for the workflow."""

    task_row_template = """
    <tr>
        <td class="border px-4 py-2">{{TASK_NAME}}</td>
        <td class="border px-4 py-2">
            <span class="px-2 py-1 rounded text-xs font-medium {{TASK_STATUS_CLASS}}">
                {{TASK_STATUS}}
            </span>
        </td>
        <td class="border px-4 py-2">{{START_TIME}}</td>
        <td class="border px-4 py-2">{{END_TIME}}</td>
        <td class="border px-4 py-2">{{DURATION}}</td>
        <td class="border px-4 py-2 text-red-600">
            {{ERROR_MESSAGE}}
        </td>
    </tr>
    """

    list_of_task_report = []

    tasks: dict[str, Task] = Registry.get_task()

    overall_status = {
        "SUCCESS": 0,
        "FAILED": 0,
        "PENDING": 0,
        "SKIPPED": 0,
    }

    total_tasks = len(tasks)
    total_duration = 0

    for task in tasks.values():
        row = task_row_template
        row = row.replace("{{TASK_NAME}}", task.name)
        row = row.replace("{{TASK_STATUS_CLASS}}", task.state.name.lower())
        row = row.replace("{{TASK_STATUS}}", task.state.name)
        row = row.replace("{{START_TIME}}", str(task.start_time))
        row = row.replace("{{END_TIME}}", str(task.end_time))
        row = row.replace("{{DURATION}}", str(task.duration))
        row = row.replace(
            "{{ERROR_MESSAGE}}",
            task.error.get_error_msg() if task.error else "",
        )

        list_of_task_report.append(row)

        overall_status[task.state.name] += 1
        total_duration += task.duration if task.duration else 0

    template = files("pravaha.report").joinpath("template.html").read_text(
        encoding="utf-8"
    )

    overall = max(overall_status, key=overall_status.get)

    template = template.replace("{{WORKFLOW_NAME}}", workflow_name)
    template = template.replace("{{EXECUTION_MODE}}", "RUNNING")
    template = template.replace("{{TOTAL_TASKS}}", str(total_tasks))
    template = template.replace("{{OVERALL_STATUS}}", overall.strip())
    template = template.replace("{{SUCCESS_COUNT}}", str(overall_status["SUCCESS"]))
    template = template.replace("{{FAILED_COUNT}}", str(overall_status["FAILED"]))
    template = template.replace("{{SKIPPED_COUNT}}", str(overall_status["SKIPPED"]))
    template = template.replace("{{TOTAL_DURATION}}", str(total_duration))
    template = template.replace(
        "{{ALL_TASK_ROW}}",
        "\n".join(list_of_task_report),
    )
    template = template.replace("{{YEAR}}", str(datetime.now().year))

    report_dir = Path.cwd() / "reports"
    report_dir.mkdir(exist_ok=True)

    template = template.replace("{{REPORT_GENERATED_AT}}", str(report_dir))

    report_file = report_dir / f"{workflow_name.strip()}.html"
    report_file.write_text(template, encoding="utf-8")
