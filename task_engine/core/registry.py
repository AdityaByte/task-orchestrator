class Registry:
    tasks = {}

    @classmethod
    def set_task(cls, name: str, task):
        if name not in cls.tasks:
            cls.tasks[name] = task

    @classmethod
    def get_task(cls):
        return cls.tasks