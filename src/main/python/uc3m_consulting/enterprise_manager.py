"""Module """
import re
import json

from datetime import datetime, timezone
from multiprocessing.managers import public_methods

from freezegun import freeze_time
from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import (PROJECTS_STORE_FILE,
                                                       TEST_DOCUMENTS_STORE_FILE,
                                                       TEST_NUMDOCS_STORE_FILE)
from uc3m_consulting.project_document import ProjectDocument

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
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

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def register_project(self,
                         company_cif: str,
                         project_acronym: str,
                         project_description: str,
                         department: str,
                         starting_date: str,
                         budget: str):
        """registers a new project"""
        new_project = EnterpriseProject(company_cif=company_cif,
                                        project_acronym=project_acronym,
                                        project_description=project_description,
                                        department=department,
                                        starting_date=starting_date,
                                        project_budget=budget)

        self.store_project(new_project)

        return new_project.project_id


    def find_docs(self, query_date):
        """
        Generates a JSON report counting valid documents for a specific date.

        Checks cryptographic hashes and timestamps to ensure historical data integrity.
        Saves the output to 'resultado.json'.

        Args:
            query_date (str): date to query.

        Returns:
            number of documents found if report is successfully generated and saved.

        Raises:
            EnterpriseManagementException: On invalid date, file IO errors,
                missing data, or cryptographic integrity failure.
        """
        EnterpriseProject.validate_date_format(query_date)

        # open documents
        documents_list = self.load_documents()

        documents_found = 0

        # loop to find
        for document_entry in documents_list:
            register_timestamp = document_entry["register_date"]

            # string conversion for easy match
            document_date = datetime.fromtimestamp(register_timestamp).strftime("%d/%m/%Y")

            if document_date == query_date:
                frozen_datetime = datetime.fromtimestamp(register_timestamp, tz=timezone.utc)
                with freeze_time(frozen_datetime):
                    # check the project id (thanks to freezetime)
                    # if project_id are different then the data has been
                    #manipulated
                    project_document = ProjectDocument(document_entry["project_id"], document_entry["file_name"])
                    if project_document.document_signature == document_entry["document_signature"]:
                        documents_found = documents_found + 1
                    else:
                        raise EnterpriseManagementException("Inconsistent document signature")

        if documents_found == 0:
            raise EnterpriseManagementException("No documents found")
        # prepare json text

        report_entry = self.build_report_entry(query_date, documents_found)
        reports_list = self.load_reports_list()
        reports_list.append(report_entry)
        self.save_reports_list(reports_list)

        return documents_found

    @staticmethod
    def build_report_entry(query_date, documents_found):
        """
        Builds the report entry for the query date.
        """
        report_timestamp = datetime.now(timezone.utc).timestamp()
        report_entry = {"Querydate": query_date,
                        "ReportDate": report_timestamp,
                        "Numfiles": documents_found
                        }
        return report_entry

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
