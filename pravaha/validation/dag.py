from pravaha.exception.validation import MissingDependencyError, CircularDependencyError

class DAGValidator:

    @staticmethod
    def validate(tasks: dict):
        visited = set()
        path_visited = set()

        # Missing dependency check.
        for task in tasks.values():
            for dep in task.depends_on:
                if dep not in tasks:
                    raise MissingDependencyError(f"Task '{task.name}' depends on missing task '{dep}'")

        # dfs cycle detection.
        def dfs(task_name, path):
            visited.add(task_name)
            path_visited.add(task_name)
            path.append(task_name)

            for dep in tasks[task_name].depends_on:
                if dep not in visited:
                    dfs(dep, path)
                elif dep in path_visited:
                    cycle = " -> ".join(path + [dep])
                    raise CircularDependencyError(f"Circular dependency detected: {cycle}")

            path_visited.remove(task_name)
            path.pop()

        # Math function where we are calling the dag.
        for task_name in tasks:
            if task_name not in visited:
                dfs(task_name, [])

        return True
