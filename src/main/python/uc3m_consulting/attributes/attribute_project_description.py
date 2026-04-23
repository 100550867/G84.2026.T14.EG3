"""Atributo para validar la descripción del proyecto."""
from uc3m_consulting.attributes.attribute import Attribute


class AttributeProjectDescription(Attribute):
    """Valida la descripción del proyecto."""

    _validation_pattern = r"^.{10,30}$"
    _error_message = "Invalid description format"
