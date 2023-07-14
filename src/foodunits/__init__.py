# read version from installed package
from importlib.metadata import version
__version__ = version("foodunits")

# populate package namespace
from foodunits.convertor import units_convertor
from foodunits.validator import units_validator
