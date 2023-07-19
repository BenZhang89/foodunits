# foodunits

Validate and convert food units with ease!

## Installation
You can install foodunits using pip:
```bash
$ pip install foodunits
```

## Usage
`foodunits` provides functionality to validate and convert food units. It supports both imperial and metric units, including common units such as "liter," "fluid ounce," "pint," "gram," "pound," as well as specific food-related units like "slice," "can," "bottle," and more.

### Validation
The validation feature checks whether a string represents a valid food unit. It is case, space, singular-plural, and full name-symbol insensitive. Only the spelling matters. It returns a boolean value indicating the validity of the unit. Here are some examples:

"Value + Unit" type strings can also be validated, such as "5 mls" or "five milliliters".

```python
from foodunits import units_validator

units_validator("fluid ounce")  # True
units_validator("fl oz")  # True
units_validator("5 fl ozs")  # True
units_validator("5 fl  ozs ")  # True
units_validator("five fl ozs")  # True
units_validator("flud ounce")  # False
units_validator("f oz")  # False
units_validator("5 l oz")  # False
units_validator("fiv fl ozs")  # False
```

### Conversation
The conversion feature allows you to convert between volumetric and mass food units, both in imperial and metric systems. For example:

```python
from foodunits import units_convertor

units_convertor("1 fluid ounce", to_unit="ml")
# Output: {"converted value": 29.573, "unit": "ml"}

units_convertor("1 1/2 fluid ounce", to_unit="ml")
# Output: {"converted value": 44.360, "unit": "ml"}
```

If you want to convert between volume and mass and have the correct conversion based on the food ingredient, you can provide the ingredient name. Currently, the package supports 100+ major ingredients. If the ingredient you input is not supported, you can provide a value for the "ingredient_density" argument. Here's an example:
```python
units_convertor("2.5", to_unit="g", from_unit="fl oz", ingredient="skimmed milk")
# Output: {"converted value": 76.152, "unit": "g"}
```

For cookery units like cup, tablespoon, and teaspoon, which depend on the country, you need to specify the country name or code:
"2.5 cups", "skimmed milk", "United States" -> "g"
```python
units_convertor("2.5 cups", to_unit="g", ingredient="skimmed milk", country="United States")
# Output: {"converted value": 618.0, "unit": "g"}
```

Note: The decimal parameter can be used to specify the number of decimal places in the converted value.

Make sure to import the relevant functions from the foodunits package to use them in your code.

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`foodunits` was created by Ben Zhang. It is licensed under the terms of the MIT license.

## Credits

`foodunits` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter). Inspired by [`validators`](https://github.com/python-validators/validators) and [`UnitConverter`](https://github.com/mattgd/UnitConverter)
