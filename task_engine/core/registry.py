class Registry:
    """
    Global registry holding all the tasks.
    """
    tasks = {}

    @classmethod
    def set_task(cls, name: str, task):
        """
        set_task: Sets the task to the global registry.
        :param name:
        :param task:
        :return:
        """
        if name not in cls.tasks:
            cls.tasks[name] = task

    @classmethod
    def get_task(cls):
        """
        Returns dictionary of tasks.
        :return dict[str, Task]
        """
        return cls.tasks