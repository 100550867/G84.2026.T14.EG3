"""
Created By Adrian Villanueva Vergara abr 2026
Universidad Carlo III de Madrid 
"""
"""Atributo para validar la fecha de inicio."""
from datetime import datetime, timezone

from uc3m_consulting.attributes.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import (
    EnterpriseManagementException,
)


class AttributeStartingDate(Attribute):
    """Valida la fecha de inicio del proyecto."""

    _validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
    _error_message = "Invalid date format"

    def _validate(self, attr_value: str) -> str:
        attr_value = super()._validate(attr_value)

        try:
            parsed_date = datetime.strptime(attr_value, "%d/%m/%Y").date()
        except ValueError as exception:
            raise EnterpriseManagementException(
                "Invalid date format"
            ) from exception

        if parsed_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException(
                "Project's date must be today or later."
            )

        if parsed_date.year < 2025 or parsed_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")

        return attr_value
