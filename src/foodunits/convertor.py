"""Module run food unit conversion"""
import re
import logging
from typing import Tuple, Dict, Any
from pattern.text.en import singularize
from foodunits.utils.utils import split_quantity_unit, validate_numeric_string, preprocess, get_ingredient_density, find_country
from foodunits.utils.units import UNITS, Convert_Dict
from foodunits.base import FoodUnitConvertor
from foodunits.exceptions import ConversionFailure


def can_convert(
    from_unit: str,
    to_unit: str,
    ingredient: str,
    ingredient_density: Tuple[int, float]
) -> Any:
    """
    Check if the given units can be converted. Currently only checks weight and volume units.
    Args:
        from_unit: The source unit to convert from
        to_unit: The target unit to convert to
        ingredient: If converting between mass and volume, ingredient or its density should be provided
        ingredient_density: If converting between mass and volume, ingredient or its density should be provided
    Returns:
        si_from_unit: The SI form of from_unit
        si_to_unit): The SI form of to_unit
    """
    acceptable_cats = ["weight", "volume"]
    _threshold =85

    # Check if units belong to acceptable categories
    from_unit_category = _find_unit_category(from_unit)
    to_unit_category = _find_unit_category(to_unit)
    if not from_unit_category or not to_unit_category or \
        from_unit_category["name"] not in acceptable_cats or \
        to_unit_category["name"] not in acceptable_cats:
        raise ConversionFailure(f"Both units should be in {acceptable_cats} category")

    if from_unit_category["name"] != to_unit_category["name"]:
        if not ingredient_density:
            ingredient_density = get_ingredient_density(
                ingredient,
                ingredient_dict = Convert_Dict.ml_to_g_by_ingredient_dict(),
                threshold = _threshold
            )
            if not ingredient_density:
                raise ConversionFailure(
                    """
                    Converstion between volume and mass.
                    Please checked the presence of arguement "ingredient" and any typos in it,
                    or specify the arguement "ingredient_density" to proceed converstion.
                    """
                )

    return get_si(from_unit), get_si(to_unit), ingredient_density


def get_si(unit: str) -> str:
    """
    Load the International System of Units (SI) string for the given unit.
    Args:
        unit: The unit for which the SI string should be loaded
    Returns:
        str: SI string or None if none was found
    """
    cat_unit = _find_unit(unit)
    if cat_unit:
        # return full name only for "cup", "teaspoon", "tablespoon"
        if cat_unit["name"] in ["cup", "teaspoon", "tablespoon"]:
            return cat_unit["name"]
        si = cat_unit["si"]
    return si if si else unit


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
    ingredient_density: float = None,
    country: str = None,
    decimal_places: int = None,
) -> Dict:
    """
    Convert the given value from the source unit to the target unit.
    Args:
        value: Value to convert, accepted forms include value only, or value + unit
               (e.g., "1 mls", just "1", 1, "one")
        from_unit: Source unit to convert from
        to_unit: Target unit to convert to
        ingredient: If converting between mass and volume, ingredient or its density should be present
        ingredient_density: If converting between mass and volume, ingredient or its density should be present
        country: Country for unit conversions (default: None)
        decimal_places: Number of decimal places for the converted value (default: None)
    Returns:
        Dict: Dictionary of converted value and unit
    """
    # import ipdb
    # ipdb.set_trace()
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
    # Check the converted value
    if not isinstance(value, (int, float)):
        raise ConversionFailure(
            f"""
            The input value {value} should be either int or float or convertable strings, such as:
                "5",
                "5.5",
                "5 fl ozs",
                "5 fluid ounces",
                "five fluid ounces",
                "5mls" etc.
            """
        )

    # Process unit; keep only alphabets and one space
    from_unit = singularize(re.sub(r"\s+", " ", re.sub(r'[^A-Za-z\s\d]+', '', from_unit)).strip())
    to_unit = singularize(re.sub(r"\s+", " ", re.sub(r'[^A-Za-z\s\d]+', '', to_unit)).strip())
    # Check if units can be converted
    # import ipdb
    # ipdb.set_trace()
    try:
        from_unit, to_unit, ingredient_density = can_convert(from_unit, to_unit, ingredient, ingredient_density)
    except ConversionFailure as e:
        # Handle the specific custom error (ConversionFailure)
        logging.error("Conversion error: %s", str(e))
        raise
    except Exception as e:
        # Handle all other exceptions
        logging.error("Exception occurred: %s", str(e))
        raise

    # Extract the numeric value from the string
    if not decimal_places:
        if "." in str(value):
            decimal_places = len(str(value)[str(value).index('.') + 1:])
        else:
            decimal_places = 0

    # Return the value if units are the same
    if from_unit == to_unit:
        return {"converted value": value, "unit": get_si(to_unit)}

    # Get the country code
    country = find_country(country)

    convertor = FoodUnitConvertor(
        value, from_unit, to_unit,
        density=ingredient_density,
        country=country,
        decimal_places=decimal_places
    )
    responses = [
        convertor.check_metric_imperial(),  # Metric and Imperial units
        convertor.check_physical_container_unit()  # Cup and Teaspoon
    ]

    for response in responses:
        if response:
            print(response)
            return response

    # Return a default response if no conversions found
    return {"converted value": None, "unit": None}
