"""Módulo para el almacenamiento de reportes"""
import json
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import TEST_NUMDOCS_STORE_FILE
from uc3m_consulting.storage.json_store import JsonStore


class ReportJsonStore(JsonStore):
    """Clase para gestionar la persistencia de reportes"""

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
