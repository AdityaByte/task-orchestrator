class ConditionContext:
    """
    Read Only execution context exposed to task conditions.
    """

    def __init__(self, env, task_states, execution_context, task_errors):
        self.env = env
        self.task_states = task_states
        self.execution_context = execution_context
        self.task_errors = task_errors