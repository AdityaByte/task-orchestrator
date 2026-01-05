from pravaha.core.task import Task
from pravaha.core.executor import TaskExecutor
from pravaha.report.report import generate_report
import os

def test_successfully_report_generation_on_valid_workflow_name(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    @Task("a")
    def a():
        pass

    TaskExecutor.execute()
    generate_report("my_report")

    report_dir = os.path.join(tmp_path, "reports")
    report_file = os.path.join(tmp_path, "reports", "my_report.html")

    assert os.path.exists(report_dir)
    assert os.path.exists(report_file)
    assert os.path.isdir(report_dir)
    assert os.path.isfile(report_file)
