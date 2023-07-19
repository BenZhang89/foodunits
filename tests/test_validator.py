"""Test food unit validator"""
# -*- coding: utf-8 -*-
import pytest
from foodunits import units_validator
from foodunits.exceptions import ValidationFailure

@pytest.mark.parametrize(
    ("value",),
    [
        ("cup",),
        ("ounces",),
        ("Fluid Ounce",),
        ("slices",),
        ("2 mls",),
        ("2mls",),
        ("2 fl ozs",),
        ("one hundred and 2 fl ozs",),
    ],
)
def test_returns_true_on_valid_food_unit(value: str):
    """Test returns true on valid food unit."""
    assert units_validator(value)

@pytest.mark.parametrize(
    ("value",),
    [
        ("",),
        ("not_a_unit",),
        ("5mlls",),
    ],
)
def test_returns_failed_validation_on_invalid_food_unit(value: str):
    """Test returns failed validation on invalid food unit."""
    assert isinstance(units_validator(value), ValidationFailure)
