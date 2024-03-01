import json
import os.path
from enum import Enum
from ipaddress import IPv4Address

from ledboardclientfull.core.project import Project
# from ledboardclientfull.core.components import Components


class ProjectPersistence:

    def new(self):
        self._update_components(Project())

    def save(self, filepath):
        project = self._project_from_components()

        def _(o):
            if isinstance(o, IPv4Address):
                return str(o)
            elif isinstance(o, Enum):
                return o.value

        with open(filepath, "w+") as project_file:
            json.dump(project.to_dict(), project_file, indent=2, default=_)

    def load(self, filepath):
        with open(filepath, "r") as project_file:
            data = json.load(project_file)

        project = Project.from_dict(data)
        self._update_components(project)

    @staticmethod
    def _update_components(project: Project):
        return
        # Components().board_communicator.set_serial_port_name(project.board_port_name)

    @staticmethod
    def _project_from_components() -> Project:
        project = Project()
        return project

        # project.board_port_name = Components().board_communicator.serial_port_name

        # return project
