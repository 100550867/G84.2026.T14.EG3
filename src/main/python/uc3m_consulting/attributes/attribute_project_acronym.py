"""
Created By Adrian Villanueva Vergara abr 2026
Universidad Carlo III de Madrid 
"""
"""Project acronym attribute."""
from uc3m_consulting.attributes.attribute import Attribute


class AttributeProjectAcronym(Attribute):
    """Validate project acronym."""

    _validation_pattern = r"^[a-zA-Z0-9]{5,10}$"
    _error_message = "Invalid acronym"
