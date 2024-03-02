import json
import logging
from enum import Enum
from ipaddress import IPv4Address

from ledboardclientfull.core.entities.project import Project
from ledboardclientfull.core.apis import APIs

_logger = logging.getLogger(__name__)


class ProjectPersistence:

    @property
    def current_project(self) -> Project:
        return self._project_from_components()

    def new(self):
        self._update_components(Project())

    def save(self, filepath):
        _logger.info(f"Save project to {filepath}")
        project = self._project_from_components()

        def _(o):
            if isinstance(o, IPv4Address):
                return str(o)
            elif isinstance(o, Enum):
                return o.value

        with open(filepath, "w+") as project_file:
            json.dump(project.to_dict(), project_file, indent=2, default=_)

    def load(self, filepath):
        _logger.info(f"Load project from {filepath}")
        with open(filepath, "r") as project_file:
            data = json.load(project_file)

        if data.get("serialization_version", 0) != 1:
            raise ValueError(f"This project is not compatible with this serialization version")

        project = Project.from_dict(data)
        self._update_components(project)

    @staticmethod
    def _update_components(project: Project):
        if project.board_configuration is not None:
            APIs().board.select_board(project.board_configuration)
        if project.board_illumination is not None:
            APIs().illumination.illuminate(project.board_illumination)

        if project.scan_capture_device_name:
            APIs().scan.set_capture_device_name(project.scan_capture_device_name)
        if project.scan_mask is not None:
            APIs().scan.set_mask(project.scan_mask)
        if project.scan_result is not None:
            APIs().scan.set_scan_result(project.scan_result)
        if project.scan_settings is not None:
            APIs().scan.set_settings(project.scan_settings)

    @staticmethod
    def _project_from_components() -> Project:
        project = Project()

        project.board_configuration = APIs().board.get_configuration()
        project.board_illumination = APIs().illumination.get_illumination()

        project.scan_capture_device_name = APIs().scan.capture_device_name()
        project.scan_mask = APIs().scan.get_mask()
        project.scan_result = APIs().scan.get_scan_result()
        project.scan_settings = APIs().scan.get_settings()

        return project
