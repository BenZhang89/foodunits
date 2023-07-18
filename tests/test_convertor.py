"""Test food unit convertor"""
# -*- coding: utf-8 -*-
import pytest
from foodunits import units_convertor
from foodunits.exceptions import ConversionFailure

def test_convert_same_unit():
    result = units_convertor(1, "ml", "ml")
    assert result == {"converted value": 1, "unit": "ml"}


@pytest.mark.parametrize(
    "value, to_unit, from_unit, country, decimal_places, expected_result",
    [
        (1, "fl oz", "ml", "US", 3, {"converted value": 0.034, "unit": "fl oz"}), # Standard input
        ("1 ml", "fl oz", None, "US", 3, {"converted value": 0.034, "unit": "fl oz"}), # Value + unit
        ("1 ml.", " fl.  oz. ", None, "US", 3, {"converted value": 0.034, "unit": "fl oz"}), # Punctuations etc.
        ("1 fluid ounce. ", " ml. ", None, "US", 3, {"converted value": 29.573, "unit": "ml"}), # Full name unit.
        ("1. 5 fluid ounce. ", " ml.", None, "US", 3, {"converted value": 44.360, "unit": "ml"}), # Float string
        ("1 1/2 fluid ounce. ", "ml. ", None, "US", 3, {"converted value": 44.360, "unit": "ml"}), # Fraction string
    ],
)
def test_convert_volume_units(value, to_unit, from_unit, country, decimal_places, expected_result):
    result = units_convertor(value, to_unit, from_unit, country=country, decimal_places=decimal_places)
    assert result == expected_result

@pytest.mark.parametrize(
    "value, to_unit, from_unit, country, decimal_places, expected_result",
    [
        (2.5, "gram", "pounds", "US", 3, {"converted value": 1133.980, "unit": "g"}), # Standard input
        ("2.5 lbs", "gram", None, "US", 3, {"converted value": 1133.980, "unit": "g"}), # Value + unit
        ("2 1/2 ounces", "grams", None, "US", 3, {"converted value": 70.874, "unit": "g"}), # Punctuations etc.
        ("2.5 stones", "kg", None, "US", 3, {"converted value": 15.876, "unit": "kg"}), # Full name unit.
        ("2. 5 drams", "g", None, "US", 3, {"converted value": 4.430, "unit": "g"}), # Float string
        (" 2.5 grains. ", "grams ", None, "US", 3, {"converted value": 0.162, "unit": "g"}), # Fraction string
    ],
)
def test_convert_mass_units(value, to_unit, from_unit, country, decimal_places, expected_result):
    result = units_convertor(value, to_unit, from_unit, country=country, decimal_places=decimal_places)
    assert result == expected_result

@pytest.mark.parametrize(
    "value, to_unit, from_unit, ingredient, ingredient_density, country, decimal_places, expected_result",
    [
        (2.5, "g", "fl oz", "water", None, "US", 3, {"converted value": 73.934, "unit": "g"}), # Standard input
        (73.934, "fl oz", "g", "water", None, "US", 3, {"converted value": 2.5, "unit": "fl oz"}),
        (73.934, "fl oz", "kg", "water", None, "US", 3, {"converted value": 2500.004, "unit": "fl oz"}),
        ("2.5 fl oz", "g", None, "skimme milk", None, "US", 3, {"converted value": 76.152, "unit": "g"}), # typo in ingredient
        ("2.5 pint", "g", None, "whole milk", 1.05, "US", 3, {"converted value": 1242.087, "unit": "g"}), # ingredient density provided.
    ],
)
def test_convert_mass_volume_units(value, to_unit, from_unit, ingredient, ingredient_density, country, decimal_places, expected_result):
    result = units_convertor(
        value, to_unit, from_unit,
        ingredient=ingredient,
        ingredient_density=ingredient_density,
        country=country,
        decimal_places=decimal_places
    )
    assert result == expected_result

@pytest.mark.parametrize(
    "value, to_unit, from_unit, ingredient, ingredient_density, country, decimal_places, expected_result",
    [
        (2.5, "ml", "cup", None, None, "US", 1, {"converted value": 600.0, "unit": "ml"}), # Standard input
        (2.5, "ml", "cup", None, None, "metric", 3, {"converted value": 625.0, "unit": "ml"}),
        ("2.5 cups", "fl oz", None, "water", None, "US", 3, {"converted value": 20.288, "unit": "fl oz"}),# cups to imperial
        ("2.5", "g", "cups", "skimmed milk", None, "united states", 3, {"converted value": 618.0, "unit": "g"}), # cups to mass
        ("2.5", "g", "cups", "skimmed milk", 1.1, "united states", 3, {"converted value": 660.0, "unit": "g"}), # cups to mass, with customized density
        ("600", "cup", "mls", "water", None, "united states", 3, {"converted value": 2.5, "unit": "cup"}), # metric to cups
        (20.288, "cup", "fl oz", "water", None, "united states", 3, {"converted value": 2.5, "unit": "cup"}), # imperial to cups
        (618, "cup", "g", "skimmed milk", None, "united states", 3, {"converted value": 2.5, "unit": "cup"}), # mass to cups
        ("2.5", "g", "tsps", "skimmed milk", None, "united states", 3, {"converted value": 12.692, "unit": "g"}), # teaspoon
        ("2.5", "g", "tbsps", "skimmed milk", None, "united states", 3, {"converted value": 38.076, "unit": "g"}), # tablespoon
    ],
)
def test_physical_container_units(value, to_unit, from_unit, ingredient, ingredient_density, country, decimal_places, expected_result):
    result = units_convertor(
        value, to_unit, from_unit,
        ingredient=ingredient,
        ingredient_density=ingredient_density,
        country=country,
        decimal_places=decimal_places
    )
    assert result == expected_result

@pytest.mark.parametrize(
    "value, to_unit, from_unit, ingredient, ingredient_density, country, decimal_places, expected_result",
    [
        ("missing value", "fl. oz", "ml", None, None, "US", 1,  ConversionFailure), # invalid value
        (2.5, "foo_to_unit", "foo_from_unit", None, None, "metric", 3,  ConversionFailure),
        (2.5, "g", "ml", "foo_ingredient", None, "US", 3,  ConversionFailure), # wrong ingredient
        (2.5, "g", "ml", None, None, "US", 3,  ConversionFailure), # missing ingredient
        (2.5, "tsp", "cup", None, None, "US", 3,  ConversionFailure), # can not convert between cup, tsp, tbsp.
        (2.5, "ml", "cup", "water", None, None, 3,  ConversionFailure), # missing country.
    ],
)
def test_convert_failure(value, to_unit, from_unit, ingredient, ingredient_density, country, decimal_places, expected_result):
    with pytest.raises(expected_result):
        units_convertor(
            value,
            to_unit,
            from_unit,
            ingredient=ingredient,
            ingredient_density=ingredient_density,
            country=country,
            decimal_places=decimal_places,
        )
