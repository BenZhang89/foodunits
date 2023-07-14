"""Utils."""
import re
from typing import Callable, Any, Tuple, List
from inspect import getfullargspec
from itertools import chain
from functools import wraps
import pycountry
from pattern.text.en import singularize
from foodunits.exceptions import ConversionFailure, ValidationFailure

def _func_args_as_dict(func: Callable[..., Any], *args: Any, **kwargs: Any):
    """Return function's positional and key-value arguments as an ordered dictionary."""
    return dict(
        list(zip(dict.fromkeys(chain(getfullargspec(func)[0], kwargs.keys())), args))
        + list(kwargs.items())
    )

def validator(func: Callable[..., Any]):
    """A decorator that makes the given function a validator.
    Whenever the given `func` returns `False`, this decorator returns a `ValidationFailure` object.
    Examples:
        >>> @validator
        ... def even(value):
        ...     return not (value % 2)
        >>> even(4)
        # Output: True
        >>> even(5)
        # Output: ValidationFailure(func=even, args={'value': 5})
    Args:
        func:
            Function to be decorated.
    Returns:
        Callable[..., ValidationFailure | bool]:
            A decorator that returns either a `ValidationFailure` object or a boolean.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        try:
            return (
                True
                if func(*args, **kwargs)
                else ValidationFailure(func, _func_args_as_dict(func, *args, **kwargs))
            )
        except Exception as exp:
            return ValidationFailure(func, _func_args_as_dict(func, *args, **kwargs), str(exp))

    return wrapper

def validate_numeric_string(input_string: str) -> Tuple[bool, float]:
    """Validate a numeric string.
    Args:
        input_string: The input string to validate.
    Returns:
        A tuple containing a boolean indicating whether the input string is numeric and the converted float value.
    """
    numeric_words = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
        "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
        "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100, "thousand": 1000, "million": 1000000,
        "billion": 1000000000,
        "and": 0,
    }
    try:
        # Try converting the input string to an integer or float
        return True, int(input_string)  # Try converting to integer
    except ValueError:
        try:
            return True, float(input_string)  # Try converting to float
        except ValueError:
            # If conversion to integer fails, check if it is a valid numeric word
            words = input_string.lower().replace('-', ' ').split()
            value = 0
            temp_value = 0
            for word in words:
                if word not in numeric_words:
                    try:
                        temp_value += int(word)
                    except ValueError:
                        return False, 0
                else:
                    if word in ["hundred", "thousand", "million", "billion"]:
                        value += temp_value * numeric_words[word]
                        temp_value = 0
                    else:
                        temp_value += numeric_words[word]
            value += temp_value
            return True, value

def split_quantity_unit(value: str) -> Tuple[str, str]:
    """Split a quantity + unit type string into quantity and unit.
    Args:
        value: The quantity + unit string to split.
    Returns:
        A tuple containing the quantity and unit.
    Type 1: Separate "fl oz(s)", "fluid ounce(s)" related unit.
        e.g., "5 fl ozs" -> ("5", "fl ozs")
              "5 fluid ounces" -> ("5", "fluid ounces")
              "five fluid ounces" -> ("five", "fluid ounces")
    Type 2: Separate word number + unit.
        e.g., "5mls" -> ("5", "mls")
    Type 3: Other quantity + unit strings.
        e.g., "5 cups" -> ("5", "cups")
              "cups" -> (None, "cups")
              "five hundreds cups" -> ("five hundreds", "cups")
    """
    # fl oz related unit
    floz_pattern = r'(.*)((?:fl|fluid)\s*(?:oz|ounce)(?:s*)$)'
    result = re.findall(floz_pattern, value)
    if result:
        return result[0][0], result[0][1]

    # quantity+unit, e.g. 5mls
    if re.match(r'\d+[a-zA-Z]+', value):
        result = re.findall(r'(\d+|[a-zA-Z]+)', value)
        return result[0], result[1]

    # others
    result = value.split(" ")
    if len(result) > 1:
        return " ".join(result[:-1]), result[-1]
    else:
        return None, result[-1]

def preprocess(value: str) -> str:
    """Preprocess a string.
    The preprocessing includes converting characters to lowercase,
    keeping only alphabets, numbers, ".", and single space,
    converting multiple spaces to one space,
    and stripping spaces from both ends.
    Args:
        value: The string to preprocess.
    Returns:
        The preprocessed string.
    """
    return re.sub(r"\s+", " ", re.sub(r'[^A-Za-z\s\d\.]+', '', value)).strip()

def find_country(country: str):
    """Find the country by name or code.
    Args:
        country: The country name or code.
    Returns:
        The country code if found, otherwise "not founded".
    """
    try:
        return pycountry.countries.search_fuzzy(country)[0].alpha_2
    except Exception as exc:
        raise ConversionFailure(f"Country {country} is not found") from exc

def find_ingredient(ingredient: str):
    """Find the ingredient by name or code.
    Args:
        ingredient: The ingredient name or code.
    Returns:
        The ingredient code if found, otherwise "not founded".
    """
    try:
        return pycountry.countries.search_fuzzy(ingredient)[0].alpha_2
    except Exception as exc:
        raise ConversionFailure(f"Ingredient {ingredient} is not found") from exc

def process_saved_units(units: List = None):
    """Process and extract saved units.
    Args:
        units: The list of units to process.
    Returns:
        A set of processed units.
    """
    # Extract and process all the saved units
    extracted_unit = [(unit['name'], unit['symbol']) for sub in units for unit in sub['units']]
    extracted_unit = [item for sublist in extracted_unit for item in sublist]
    units_processed = set([singularize(unit.lower().replace(" ", "")) for unit in extracted_unit])
    return units_processed
