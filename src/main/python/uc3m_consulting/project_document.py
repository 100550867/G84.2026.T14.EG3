"""Contains the class ProjectDocument"""
import hashlib
from datetime import datetime, timezone
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class ProjectDocument:
    """Class representing the information required for a project document"""

    def __init__(self, project_id: str, file_name: str, registration_date: float = None):
        self.__alg = "SHA-256"
        self.__type = "PDF"
        self.__project_id = project_id
        self.__file_name = file_name
        # Si nos dan una fecha (del JSON), la usamos. Si no, usamos la de ahora.
        if registration_date:
            self.__register_date = registration_date
        else:
            justnow = datetime.now(timezone.utc)
            self.__register_date = datetime.timestamp(justnow)

    @classmethod
    def create_and_validate_from_entry(cls, document_entry):
        """Metodo de clase para instanciar y validar usando la fecha del JSON"""
        p_id = document_entry.get("project_id")
        f_name = document_entry.get("file_name")
        expected_sig = document_entry.get("document_signature")
        # CLAVE: Extraemos la fecha del JSON para que la firma coincida
        r_date = document_entry.get("register_date")

        # Pasamos r_date al constructor
        my_doc = cls(p_id, f_name, r_date)

        if my_doc.document_signature != expected_sig:
            raise EnterpriseManagementException("Inconsistent document signature")

        return my_doc

    def to_json(self):
        """returns the object data in json format"""
        return {"alg": self.__alg,
                "type": self.__type,
                "project_id": self.__project_id,
                "file_name": self.__file_name,
                "register_date": self.__register_date,
                "document_signature": self.document_signature}

    def __signature_string(self):
        """Composes the string to be used for generating the key"""
        return "{alg:" + str(self.__alg) +",typ:" + str(self.__type) +",project_id:" + \
               str(self.__project_id) + ",file_name:" + str(self.__file_name) + \
               ",register_date:" + str(self.__register_date) + "}"

    @property
    def project_id(self):
        """Property that represents the project_id"""
        return self.__project_id

    @project_id.setter
    def project_id(self, value):
        self.__project_id = value

    @property
    def file_name(self):
        """Property that represents the file_name"""
        return self.__file_name

    @file_name.setter
    def file_name(self, value):
        self.__file_name = value

    @property
    def register_date(self):
        """Property that represents the register date"""
        return self.__register_date

    @property
    def document_signature(self):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()
