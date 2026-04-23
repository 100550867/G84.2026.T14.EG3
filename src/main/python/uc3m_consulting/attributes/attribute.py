"""Base class for attribute validation."""
import re

from uc3m_consulting.enterprise_management_exception import (
    EnterpriseManagementException,
)

# pylint: disable=too-few-public-methods
class Attribute:
    """Generic attribute validator."""

    _validation_pattern = None
    _error_message = "Invalid value"

    def __init__(self, attr_value: str):
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value: str) -> str:
        """Validate attribute using the class regex."""
        if not isinstance(attr_value, str):
            raise EnterpriseManagementException(self._error_message)

        if self._validation_pattern is None:
            raise EnterpriseManagementException("Validation pattern not defined")

        if not re.fullmatch(self._validation_pattern, attr_value):
            raise EnterpriseManagementException(self._error_message)

        return attr_value

    @property
    def value(self) -> str:
        """Return validated value."""
        return self._attr_value
