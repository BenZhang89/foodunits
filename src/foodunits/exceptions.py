"""Exceptions"""
from typing import Callable, Dict, Any

class ValidationFailure(Exception):
    """Exception class for validation failures."""

    def __init__(self, function: Callable[..., Any], arg_dict: Dict[str, Any], message: str = ""):
        """Initialize ValidationFailure."""
        if message:
            self.reason = message
        self.func = function
        self.__dict__.update(arg_dict)

    def __repr__(self):
        """Return the string representation of ValidationFailure."""
        return (
            f"ValidationFailure(func={self.func.__name__}, "
            + f"args={({k: v for (k, v) in self.__dict__.items() if k != 'func'})})"
        )

    def __str__(self):
        """Return the string representation of ValidationFailure."""
        return repr(self)

    def __bool__(self):
        """Return False for ValidationFailure."""
        return False

class ConversionFailure(Exception):
    """
    Exception class indicating that a conversion is not possible.
    """

    def __init__(self, reason: str):
        self.reason = reason

    def __repr__(self):
        """Return the string representation of ConversionFailure."""
        return f"ConversionFailure: {self.reason}"
