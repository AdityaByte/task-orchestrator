class Dependency:
    def __init__(self, type: str = "", dependencies: list[str] = []):
        self.type = type
        self.dependencies = dependencies

    def get_type(self):
        return self.name

    def get_dependencies(self):
        return self.dependencies