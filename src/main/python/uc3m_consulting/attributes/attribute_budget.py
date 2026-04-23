"""
Created By Adrian Villanueva Vergara abr 2026
Universidad Carlo III de Madrid 
"""
"""Atributo para validar el presupuesto."""
from uc3m_consulting.attributes.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import (
    EnterpriseManagementException,
)


class AttributeBudget(Attribute):
    """Valida el presupuesto del proyecto."""

    def _validate(self, attr_value: str) -> str:
        if not isinstance(attr_value, str):
            raise EnterpriseManagementException("Invalid budget amount")

        try:
            budget_amount = float(attr_value)
        except ValueError as exception:
            raise EnterpriseManagementException(
                "Invalid budget amount"
            ) from exception

        budget_as_text = str(budget_amount)
        if "." in budget_as_text:
            decimal_places = len(budget_as_text.split(".")[1])
            if decimal_places > 2:
                raise EnterpriseManagementException("Invalid budget amount")

        if budget_amount < 50000 or budget_amount > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")

        return attr_value