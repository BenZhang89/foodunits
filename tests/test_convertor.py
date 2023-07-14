"""Test food unit convertor"""
# -*- coding: utf-8 -*-
# import pytest
from foodunits.convertor import units_convertor
# from exceptions import ConversionFailure

def test_convert_same_unit():
    result = units_convertor(1, "ml", "ml")
    assert result == {"converted value": 1, "unit": "ml"}

# def test_convert_volume_units():
#     result = units_convertor(1, "fl oz", "ml", country="US", decimal_places=3)
#     assert result == {"converted value": 0.034, "unit": "fl oz"}

#     result = units_convertor("1 ml", "fl oz", country="US", decimal_places=3)
#     assert result == {"converted value": 0.034, "unit": "fl oz"}

# def test_convert_mass_volume_units():
#     result = units_convertor(100, "g", "ml", ingredient="water")
#     assert result == {"converted value": 100, "unit": "ml"}

#     result = units_convertor(100, "ml", "g", ingredient="water")
#     assert result == {"converted value": 100, "unit": "g"}

# def test_convert_invalid_units():
#     result = units_convertor(1, "invalid_unit", "ml")
#     assert result == {"converted value": None, "unit": None}

# def test_convert_invalid_value():
#     result = units_convertor("invalid_value", "ml", "fl oz")
#     assert result == {"converted value": None, "unit": None}
