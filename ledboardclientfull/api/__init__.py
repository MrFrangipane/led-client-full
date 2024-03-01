from ledboardclientfull.components.project_persistence import ProjectPersistence
from ledboardclientfull.core.components import Components


def init_ledboard_client():
    Components().project_persistence = ProjectPersistence()
