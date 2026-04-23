"""Module """


from datetime import datetime, timezone

from freezegun import freeze_time
from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.project_document import ProjectDocument
from uc3m_consulting.json_store import JsonStore

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""

    instance = None

    def __new__(cls):
        if not EnterpriseManager.instance:
            EnterpriseManager.instance = super(EnterpriseManager, cls).__new__(cls)

        return EnterpriseManager.instance

    def __init__(self):
        pass


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

        JsonStore().store_project(new_project)

        return new_project.project_id

    def find_docs(self, query_date):
        """
        Generates a JSON report counting valid documents for a specific date.
        """
        EnterpriseProject.validate_date_format(query_date)

        documents_list = JsonStore().load_documents()
        documents_found = self.count_valid_documents(documents_list,
                                                     query_date)

        if documents_found == 0:
            raise EnterpriseManagementException("No documents found")

        report_entry = self.build_report_entry(query_date, documents_found)
        reports_list = JsonStore().load_reports_list()
        reports_list.append(report_entry)
        JsonStore().save_reports_list(reports_list)

        return documents_found

    @staticmethod
    def is_document_from_query_date(document_entry, query_date):
        """
        Check whether the document was registered on the query date
        """
        register_timestamp = document_entry["register_date"]
        document_date = datetime.fromtimestamp(register_timestamp).strftime(
            "%d/%m/%Y")
        return document_date == query_date

    @staticmethod
    def check_document_signature(document_entry):
        """
        Check document signature consistency
        """
        register_timestamp = document_entry["register_date"]
        frozen_datetime = datetime.fromtimestamp(register_timestamp,
                                                 tz=timezone.utc)

        with freeze_time(frozen_datetime):
            project_document = ProjectDocument(
                document_entry["project_id"],
                document_entry["file_name"]
            )
            if project_document.document_signature != document_entry[
                "document_signature"]:
                raise EnterpriseManagementException(
                    "Inconsistent document signature")

    def count_valid_documents(self, documents_list, query_date):
        """
        Count valid documents registered on the given date
        """
        documents_found = 0

        for document_entry in documents_list:
            if self.is_document_from_query_date(document_entry, query_date):
                self.check_document_signature(document_entry)
                documents_found += 1

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

