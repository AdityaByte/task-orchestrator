from argparse import Namespace
from task_engine.core.registry import Registry
from task_engine.core.executor import TaskExecutor
from task_engine.report.report import generate_report

import importlib
import importlib.util
import sys
from pathlib import Path


def run(args: Namespace):
    # Later on we will add more positional arg to it but
    # for now we are only expecting run only.
    if args.command != "run":
        return

    if args.file:
        _load_from_file(args.file)
    elif args.module:
        _load_from_module(args.module)

    if not Registry.get_task():
        raise RuntimeError(
            "No tasks were registered. "
            "Make sure your file/module defines @Task decorators."
        )

    TaskExecutor.execute(
        tags=tuple(args.tags or ()),
        taskgroup=tuple(args.task_group or ())
    )

    if args.report:
        generate_report(args.report)


def _load_from_file(path: str) -> None:
    """Importing workflow file."""
    path = Path(path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"Workflow file not found: {path}")

    module_name = path.stem

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load file: {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)


def _load_from_module(module_path: str) -> None:
    """Importing the whole module."""
    try:
        importlib.import_module(module_path)
    except ImportError as e:
        raise RuntimeError(f"Cannot import module: {module_path}") from e
