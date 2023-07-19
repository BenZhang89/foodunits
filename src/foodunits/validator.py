# -*- coding: utf-8 -*-
"""foodunit validator"""
import warnings
from typing import List
from pattern.text.en import singularize
from foodunits.utils.units import UNITS
from foodunits.utils.utils import validator, split_quantity_unit, validate_numeric_string, preprocess, process_saved_units

@validator
def units_validator(
    value: str,
    units: List[str] = None,
):
    """
    Validate a food unit address.
    This is inspired by the `python-validators` library.

    Args:
        value:
            Food unit string to validate.
        units:
            Legitimate food units.

    Returns:
        bool:
            True if `value` is a valid food unit.
        ValidationFailure:
            If `value` is an invalid food unit.

    Examples:
        >>> unit_validator('5 mls')
        # Output: True
        >>> unit_validator('ml')
        # Output: True
        >>> unit_validator('five mls')
        # Output: True
        >>> unit_validator('5mls')
        # Output: True (with Warning Message)
        >>> unit_validator('mlls')
        # Output: ValidationFailure(func=unit_validator, args={'value': 'mlls'})

    """
    if not value:
        return False

    if units is None:
        units = UNITS

    units_processed = process_saved_units(units)
    cleaned_value = preprocess(value)
    quantity, unit = split_quantity_unit(cleaned_value)
    # Remove spaces and periods, and singularize the unit
    unit = singularize(unit.replace(" ", "").replace(".", ""))

    if quantity:
        valid, _ = validate_numeric_string(quantity)
        if valid:
            # Display a warning
            warnings.warn(f"This food unit {value} contains quantity")
            return unit in units_processed
        else:
            return False
    else:
        return unit in units_processed
