"""Módulo para el almacenamiento de proyectos"""
# pylint: disable=too-few-public-methods
import json
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import PROJECTS_STORE_FILE
from uc3m_consulting.storage.json_store import JsonStore


class ProjectJsonStore(JsonStore):
    """Clase para gestionar la persistencia de proyectos"""

    @staticmethod
    def store_project(new_project):
        """
        Store a project in the JSON file, checking duplicates
        """
        try:
            with open(PROJECTS_STORE_FILE, "r", encoding="utf-8",
                      newline="") as file:
                projects_list = json.load(file)
        except FileNotFoundError:
            projects_list = []
        except json.JSONDecodeError as exception:
            raise EnterpriseManagementException(
                "JSON Decode Error - Wrong JSON Format") from exception

        for stored_project in projects_list:
            if stored_project == new_project.to_json():
                raise EnterpriseManagementException(
                    "Duplicated project in projects list")

        projects_list.append(new_project.to_json())

        try:
            with open(PROJECTS_STORE_FILE, "w", encoding="utf-8",
                      newline="") as file:
                json.dump(projects_list, file, indent=2)
        except FileNotFoundError as exception:
            raise EnterpriseManagementException(
                "Wrong file  or file path") from exception
        except json.JSONDecodeError as exception:
            raise EnterpriseManagementException(
                "JSON Decode Error - Wrong JSON Format") from exception
