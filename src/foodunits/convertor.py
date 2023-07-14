"""Module run food unit conversion"""
import re
from typing import Tuple, Dict
from foodunits.utils.utils import split_quantity_unit, validate_numeric_string, preprocess
from foodunits.utils.units import UNITS
from foodunits.base import FoodUnitConvertor
from foodunits.exceptions import ConversionFailure


def can_convert(value: Tuple[int, float], from_unit: str, to_unit: str, ingredient: str) -> bool:
    """
    Check if the given units can be converted. Currently only checks weight and volume units.
    Args:
        value: The quantity value
        from_unit: The source unit to convert from
        to_unit: The target unit to convert to
        ingredient: If converting between mass and volume, ingredient should be provided
    Returns:
        bool: True if units can be converted, False otherwise
    """
    acceptable_cats = ["weight", "volume"]

    if not isinstance(value, (int, float)):
        raise ConversionFailure(f"The processed value {value} should be either int or float, not {type(value)}")

    # Check if units belong to acceptable categories
    from_unit_category = _find_unit_category(from_unit)
    to_unit_category = _find_unit_category(to_unit)

    if from_unit_category["name"] not in acceptable_cats or to_unit_category["name"] not in acceptable_cats:
        raise ConversionFailure(f"Both units should be in {acceptable_cats} category")

    if from_unit_category["name"] != to_unit_category["name"]:
        if not ingredient:
            raise ConversionFailure("Since units are in different categories, ingredient should be provided")

    return True


def get_si(unit: str) -> str:
    """
    Load the International System of Units (SI) string for the given unit.
    Args:
        unit: The unit for which the SI string should be loaded
    Returns:
        str: SI string or None if none was found
    """
    cat_unit = _find_unit(unit)
    return cat_unit["si"] if cat_unit else None


def _find_unit_category(unit: str) -> Dict:
    """
    Internal: Load the category of one unit from the UNITS array.
    Args:
        unit: The unit which should be included in the '_internal_accepted_names'
            in a category of the UNITS array
    Returns:
        Dict: The category from the UNITS array or None if none was found
    """
    for category in UNITS:
        for cat_unit in category["units"]:
            if unit == cat_unit["name"] or unit == cat_unit["si"]:
                return category
    return None


def _find_unit(unit: str) -> Dict:
    """
    Internal: Load one specific unit from the UNITS array.
    Args:
        unit: The name of the unit (should be included in the '_internal_accepted_names' or 'name')
    Returns:
        Dict: The unit from the UNITS array or None if none was found
    """
    for category in UNITS:
        for cat_unit in category["units"]:
            if unit == cat_unit["name"] or unit == cat_unit["si"]:
                return cat_unit
    return None


def units_convertor(
    value: Tuple[str, int, float],
    to_unit: str,
    from_unit: str = None,
    ingredient: str = None,
    country: str = "US",
    decimal_places: int = 2,
) -> Dict:
    """
    Convert the given value from the source unit to the target unit.
    Args:
        value: Value to convert, accepted forms include value only, or value + unit
               (e.g., "1 mls", just "1", 1, "one")
        from_unit: Source unit to convert from
        to_unit: Target unit to convert to
        ingredient: If converting between mass and volume, ingredient should be present
        country: Country for unit conversions (default: "US")
        decimal_places: Number of decimal places for the converted value (default: 2)
    Returns:
        Dict: Dictionary of converted value and unit
    """
    # Convert string input to value or value + unit
    if isinstance(value, str):
        cleaned_value = preprocess(value)
        valid, valid_value = validate_numeric_string(cleaned_value)
        if valid:
            value = valid_value
        else:
            value, unit_split = split_quantity_unit(cleaned_value)
            valid, valid_value = validate_numeric_string(value)
            from_unit = from_unit if from_unit else unit_split
            value = valid_value if valid else None

    # Process unit; keep only alphabets and one space
    from_unit = re.sub(r"\s+", " ", re.sub(r'[^A-Za-z\s\d]+', '', from_unit)).strip()
    to_unit = re.sub(r"\s+", " ", re.sub(r'[^A-Za-z\s\d]+', '', to_unit)).strip()

    # Check if units can be converted
    can_convert(value, from_unit, to_unit, ingredient)

    # Extract the numeric value from the string
    if "." in str(value):
        decimal_places = len(str(value)[str(value).index('.') + 1:])

    # Return the value if units are the same
    if from_unit == to_unit:
        return {"converted value": value, "unit": get_si(to_unit)}

    convertor = FoodUnitConvertor(value, from_unit, to_unit, decimal_places, ingredient=ingredient, country=country)

    responses = [
        convertor.check_metric_imperial(),  # Metric and Imperial units
        convertor.check_physical_container_unit()  # Cup and Teaspoon
    ]

    for response in responses:
        if response:
            return response

    # Return a default response if no conversions found
    return {"converted value": None, "unit": None}
