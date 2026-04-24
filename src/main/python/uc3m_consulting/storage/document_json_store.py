"""Módulo para la lectura de documentos"""
# pylint: disable=too-few-public-methods
import json
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import TEST_DOCUMENTS_STORE_FILE
from uc3m_consulting.storage.json_store import JsonStore


class DocumentJsonStore(JsonStore):
    """Clase para gestionar la lectura de documentos"""

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
