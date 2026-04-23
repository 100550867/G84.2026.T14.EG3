"""Atributo para validar el CIF."""
from uc3m_consulting.attributes.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import (
    EnterpriseManagementException,
)


class AttributeCif(Attribute):
    """Valida el CIF."""

    _validation_pattern = r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$"
    _error_message = "Invalid CIF format"

    def _validate(self, attr_value: str) -> str:
        attr_value = super()._validate(attr_value)

        cif_letter = attr_value[0]
        cif_numbers = attr_value[1:8]
        cif_last_character = attr_value[8]

        even_positions_sum = 0
        odd_positions_sum = 0

        for index, digit in enumerate(cif_numbers):
            if index % 2 == 0:
                doubled_digit = int(digit) * 2
                if doubled_digit > 9:
                    even_positions_sum += (
                                                  doubled_digit // 10
                                          ) + (
                                                  doubled_digit % 10
                                          )
                else:
                    even_positions_sum += doubled_digit
            else:
                odd_positions_sum += int(digit)

        total_sum = even_positions_sum + odd_positions_sum
        control_digit = 10 - (total_sum % 10)

        if control_digit == 10:
            control_digit = 0

        control_letters = "JABCDEFGHI"

        if cif_letter in ("A", "B", "E", "H"):
            if str(control_digit) != cif_last_character:
                raise EnterpriseManagementException(
                    "Invalid CIF character control number"
                )
        elif cif_letter in ("P", "Q", "S", "K"):
            if control_letters[control_digit] != cif_last_character:
                raise EnterpriseManagementException(
                    "Invalid CIF character control letter"
                )
        else:
            raise EnterpriseManagementException("CIF type not supported")

        return attr_value
