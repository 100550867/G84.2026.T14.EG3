"""MODULE: enterprise_project. Contains the EnterpriseProject class"""
import hashlib
import json
import re
from datetime import datetime, timezone
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class EnterpriseProject:
    """Class representing a project"""
    #pylint: disable=too-many-arguments, too-many-positional-arguments
    def __init__(self,
                 company_cif: str,
                 project_acronym: str,
                 project_description: str,
                 department: str,
                 starting_date: str,
                 project_budget: float):
        self.__company_cif = self.validate_cif(company_cif)
        self.__project_description = project_description
        self.__project_achronym = self.validate_project_acronym(project_acronym)
        self.__department = department
        self.__starting_date = starting_date
        self.__project_budget = project_budget
        justnow = datetime.now(timezone.utc)
        self.__time_stamp = datetime.timestamp(justnow)

    def __str__(self):
        return "Project:" + json.dumps(self.__dict__)

    def to_json(self):
        """returns the object information in json format"""
        return {
            "company_cif": self.__company_cif,
            "project_description": self.__project_description,
            "project_acronym": self.__project_achronym,
            "project_budget": self.__project_budget,
            "department": self.__department,
            "starting_date": self.__starting_date,
            "time_stamp": self.__time_stamp,
            "project_id": self.project_id
        }
    @property
    def company_cif(self):
        """Company's cif"""
        return self.__company_cif

    @company_cif.setter
    def company_cif(self, value):
        self.__company_cif = value

    @property
    def project_description(self):
        """Property representing the project description"""
        return self.__project_description

    @project_description.setter
    def project_description(self, value):
        self.__project_description = value

    @property
    def project_acronym(self):
        """Property representing the acronym"""
        return self.__project_achronym
    @project_acronym.setter
    def project_acronym(self, value):
        self.__project_achronym = value

    @property
    def project_budget(self):
        """Property respresenting the project budget"""
        return self.__project_budget
    @project_budget.setter
    def project_budget(self, value):
        self.__project_budget = value

    @property
    def department(self):
        """Property representing the department"""
        return self.__department
    @department.setter
    def department(self, value):
        self.__department = value

    @property
    def starting_date( self ):
        """Property representing the project's date"""
        return self.__starting_date
    @starting_date.setter
    def starting_date( self, value ):
        self.__starting_date = value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def project_id(self):
        """Returns the md5 signature (project id)"""
        return hashlib.md5(str(self).encode()).hexdigest()

    @staticmethod
    def validate_cif(company_cif: str):
        """validates a cif number """
        if not isinstance(company_cif, str):
            raise EnterpriseManagementException("CIF code must be a string")

        cif_pattern = re.compile(r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$")
        if not cif_pattern.fullmatch(company_cif):
            raise EnterpriseManagementException("Invalid CIF format")

        cif_letter = company_cif[0]
        cif_numbers = company_cif[1:8]
        cif_last_character = company_cif[8]

        even_positions_sum = 0
        odd_positions_sum = 0

        for index in range(len(cif_numbers)):
            if index % 2 == 0:
                doubled_digit = int(cif_numbers[index]) * 2
                if doubled_digit > 9:
                    even_positions_sum = even_positions_sum + (
                                doubled_digit // 10) + (doubled_digit % 10)
                else:
                    even_positions_sum = even_positions_sum + doubled_digit
            else:
                odd_positions_sum = odd_positions_sum + int(cif_numbers[index])

        total_sum = even_positions_sum + odd_positions_sum
        last_digit = total_sum % 10
        control_digit = 10 - last_digit

        if control_digit == 10:
            control_digit = 0

        control_letters = "JABCDEFGHI"

        if cif_letter in ('A', 'B', 'E', 'H'):
            if str(control_digit) != cif_last_character:
                raise EnterpriseManagementException(
                    "Invalid CIF character control number")
        elif cif_letter in ('P', 'Q', 'S', 'K'):
            if control_letters[control_digit] != cif_last_character:
                raise EnterpriseManagementException(
                    "Invalid CIF character control letter")
        else:
            raise EnterpriseManagementException("CIF type not supported")

        return company_cif

    @staticmethod
    def validate_project_acronym(project_acronym: str) -> str:
        """
        Validate project acronym
        """
        acronym_pattern = re.compile(r"^[a-zA-Z0-9]{5,10}$")
        if not acronym_pattern.fullmatch(project_acronym):
            raise EnterpriseManagementException("Invalid acronym")
        return project_acronym
