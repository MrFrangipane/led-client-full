from ledboardclientfull.core.components import Components
from ledboardclientfull.core.entities.project import Project


def current_project() -> Project:
    return Components().project_persistence.current_project


def new() -> None:
    Components().project_persistence.new()


def save(filepath) -> None:
    Components().project_persistence.save(filepath)


def load(filepath) -> None:
    if Components().project_persistence is None:
        raise RuntimeError("LEDBoard client is not initialized")

    Components().project_persistence.load(filepath)
