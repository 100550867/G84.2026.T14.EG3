"""Project acronym attribute."""
from uc3m_consulting.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class AttributeProjectAcronym(Attribute):
    """Validate project acronym."""

    _validation_pattern = r"^[a-zA-Z0-9]{5,10}$"
    _error_message = "Invalid acronym"
