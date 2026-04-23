"""Atributo para validar el departamento."""
from uc3m_consulting.attributes.attribute import Attribute


class AttributeDepartment(Attribute):
    """Valida el departamento."""

    _validation_pattern = r"^(HR|FINANCE|LEGAL|LOGISTICS)$"
    _error_message = "Invalid department"
