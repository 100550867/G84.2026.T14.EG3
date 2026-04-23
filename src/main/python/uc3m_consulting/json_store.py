"""Modulo para manejar los JSON de almacenamiento"""
import json
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import (PROJECTS_STORE_FILE,
                                                       TEST_DOCUMENTS_STORE_FILE,
                                                       TEST_NUMDOCS_STORE_FILE)


class JsonStore:
    """Class for managing data files"""

    # 1. Aplicamos el Singleton igual que antes
    instance = None

    def __new__(cls):
        if not JsonStore.instance:
            JsonStore.instance = super(JsonStore, cls).__new__(cls)
        return JsonStore.instance

    def __init__(self):
        pass

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

    @staticmethod
    def load_reports_list():
        """
        Loads the reports lists from the JSON file
        """
        try:
            with open(TEST_NUMDOCS_STORE_FILE, "r", encoding="utf-8",
                      newline="") as file:
                reports_list = json.load(file)
        except FileNotFoundError:
            reports_list = []
        except json.JSONDecodeError as exception:
            raise EnterpriseManagementException(
                "JSON Decode Error - Wrong JSON Format") from exception
        return reports_list

    @staticmethod
    def load_documents():
        """
        Loads documents from the JSON file
        """
        try:
            with open(TEST_DOCUMENTS_STORE_FILE, "r", encoding="utf-8",
                      newline="") as file:
                documents_list = json.load(file)
        except FileNotFoundError as exception:
            raise EnterpriseManagementException(
                "Wrong file  or file path") from exception
        return documents_list

    @staticmethod
    def save_reports_list(reports_list):
        """
        Saves reports list in the JSON file.
        """
        try:
            with open(TEST_NUMDOCS_STORE_FILE, "w", encoding="utf-8",
                      newline="") as file:
                json.dump(reports_list, file, indent=2)
        except FileNotFoundError as exception:
            raise EnterpriseManagementException(
                "Wrong file  or file path") from exception
