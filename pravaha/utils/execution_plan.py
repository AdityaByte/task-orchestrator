from pravaha.core.registry import Registry

def dry_run():
    """
    Return the execution order of tasks as a list.

    This class method simulates task execution without running them,
    useful for validation and debugging.

    Returns
    -------
    list of str
        Ordered list of task names in execution sequence.
    """
    final_output = []

    tasks = Registry.get_task()
    for task in tasks.values():
        if task.depends_on is not None and task.depends_on != []:
            final_output.append(f"{task.name} - depends on ({','.join(task.depends_on)})")
        else:
            final_output.append(f"{task.name} - no dependencies ")

    if not final_output:
        return "Dry Run Results:\nNo tasks found."

    return f"Dry Run Results:\n{chr(10).join(map(str, final_output))}"