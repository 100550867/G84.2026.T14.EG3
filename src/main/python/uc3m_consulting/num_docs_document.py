"""Módulo para la clase NumDocsDocument"""
from datetime import datetime, timezone

class NumDocsDocument:
    """Clase que representa el contenido de un reporte de documentos"""
    def __init__(self, query_date, num_files):
        self.__query_date = query_date
        self.__num_files = num_files
        self.__report_date = datetime.now(timezone.utc).timestamp()

    @property
    def query_date(self):
        """Getter para la fecha de consulta"""
        return self.__query_date

    @property
    def num_files(self):
        """Getter para el número de archivos"""
        return self.__num_files

    def to_json(self):
        """Convierte el objeto a formato diccionario para JSON"""
        return {
            "Querydate": self.__query_date,
            "ReportDate": self.__report_date,
            "Numfiles": self.__num_files
        }
