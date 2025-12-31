import argparse

def build_parser():
    parser = argparse.ArgumentParser(
        prog="Task Orchestrator",
        description="A workflow automation tool for automating tasks",
        epilog="@Author: Aditya Pawar"
    )

    sub_parsers = parser.add_subparsers(dest="command", required=True)

    run_parser = sub_parsers.add_parser(
        "run",
        help = "Run tasks from a file or module"
    )

    source_group = run_parser.add_mutually_exclusive_group(required=True)

    source_group.add_argument(
        "--file",
        help = "Path to python file containing workflow"
    )

    source_group.add_argument(
        "--module",
        help = "Path of the python module containing several workflows"
    )

    # Execution modifiers.
    run_parser.add_argument(
        "--report",
        help = "File name without extension (e.g: task_report)"
    )

    run_parser.add_argument(
        "--tags",
        help = "Comma separated list of tags. (eg: dev,prod)"
    )

    run_parser.add_argument(
        "--task-group",
        help = "Comma seperated list of task group."
    )

    return parser


def parse_args():
    parser = build_parser()
    args = parser.parse_args()

    if args.tags:
        args.tags = [t.strip() for t in args.tags.split(",") if t.strip()]

    if args.task_group:
        args.task_group = [tg.strip() for tg in args.task_group.split(",") if tg.strip()]

    return args