"""Food unit and conversion rate dictionary"""
# -*- coding: utf-8 -*-
class Dictionary():
    """
    Convertion rate
    """
    # Metric and Imperial systems
    __metric_dict = {
        'E': 1000000000000000000,
        'P': 1000000000000000,
        'T': 1000000000000,
        'G': 1000000000,
        'M': 1000000,
        'k': 1000,
        'h': 100,
        'da': 10,
        None: 1,
        'd': .1,
        'c': .01,
        'm': .001,
        'μ': .000001,
        'n': .000000001,
        'p': .000000000001,
        'f': .000000000000001,
        'a': .000000000000000001
    }
    __imperial_vol_dict = {
        'gal': 128,
        'qt': 32,
        'pt': 16,
        'gi': 4,
        'floz': 1
    }
    __imperial_mass_dict = {
        't': 2240,
        'cwt': 112,
        'qr': 28,
        'qtr': 28,
        'st': 14,
        'lb': 1,
        'oz': .0625,
        'dr': .00390625,
        'gr': .00014285714
    }

    __cup_by_country_dict = {
        'metric': 0.25,
        'international': 0.25,
        'other': 0.25,
        'us': 0.24,
        'us legal': 0.24,
        'us customary': 0.2365882365,
        'ca': 0.25,
        'uk': 0.2841,
        'jp': 0.2,
        'kr': 0.2,
        'ru': 0.246,
    } # to be expend

    __teaspoon_by_country_dict = {
        'metric': 0.005,
        'international': 0.005,
        'other': 0.005,
        'us': 0.00492892,
        'imperial': 0.005919,
    } # to be expend

    __tablespoon_by_country_dict = {
        'metric': 0.005,
        'international': 0.005,
        'other': 0.005,
        'us': 0.00492892,
        'imperial': 0.005919,
    } # to be expend

    # add custom conversion rate
    __ml_to_g_by_ingredient_dict = {
        "water": 1, # water
        "flour": 0.529, # flour
        "all-purpose flour": 0.529,
        "almond flour": 0.406,
        "bread flour": 0.55,
        "cake flour": 0.482,
        "coconut flour": 0.51,
        "corn flour": 0.65,
        "chickpea flour": 0.58,
        "oat flour": 0.64,
        "pastry flour": 0.448,
        "whole wheat flour": 0.478,
        "baking powder": 0.9,
        "baking soda": 0.69,
        "cream of tartar": 0.68,
        "sourdough starter": 0.972,
        "granulated sugar": 0.85, # sugars and sweetners
        "brown sugar": 0.95,
        "powdered sugar": 0.65,
        "honey": 1.42,
        "maple syrup": 1.35,
        "agave nectar": 1.4,
        "molasses": 1.45,
        "corn syrup": 1.38,
        "coconut sugar": 0.9,
        "stevia (powder)": 0.12,
        "butter": 0.911, # fats and oils
        "vegetable oil": 0.920,
        "olive oil": 0.920,
        "canola oil": 0.922,
        "coconut oil": 0.924,
        "sunflower oil": 0.924,
        "sesame oil": 0.929,
        "peanut oil": 0.924,
        "lard": 0.859,
        "shortening": 0.918,
        "almond milk": 1.04, # milk and cream
        "buttermilk": 1.01,
        "cashew milk": 1.03,
        "coconut milk": 1.02,
        "condensed milk": 1.28,
        "evaporated milk": 1.14,
        "half-and-half": 1.011,
        "heavy cream": 1.007,
        "light cream": 1.011,
        "oat milk": 1.03,
        "rice milk": 1.03,
        "semi-skimmed milk": 1.03,
        "skimmed milk": 1.03,
        "soy milk": 1.02,
        "whipping cream": 1.011,
        "whole milk": 1.03,
        "almonds": 0.595,  # nuts and seeds
        "cashews": 0.585,
        "chia seeds": 0.555,
        "flaxseeds": 0.525,
        "hazelnuts": 0.655,
        "pecans": 0.625,
        "pine nuts": 0.595,
        "pistachios": 0.605,
        "poppy seeds": 0.605,
        "sesame seeds": 0.585,
        "sunflower seeds": 0.580,
        "walnuts": 0.595,
        "apples": 0.960, # fruits and vegs
        "bananas": 0.950,
        "blueberries": 0.840,
        "carrots": 0.810,
        "grapes": 0.810,
        "lemons": 0.960,
        "onions": 0.870,
        "oranges": 0.930,
        "potatoes": 0.775,
        "spinach": 0.760,
        "strawberries": 0.780,
        "tomatoes": 0.940,
        "watermelons": 0.960,
        "salt": 1.20, # other major ingredients
        "black pepper": 0.62,
        "garlic (minced)": 1.20,
        "onion (diced)": 0.80,
        "white vinegar": 1.04,
        "soy sauce": 1.03,
        "mustard": 1.12,
        "ketchup": 1.40,
        "mayonnaise": 0.94,
        "egg (whole)": 1.06,
        "bacon (cooked)": 0.70,
        "shrimp (peeled and deveined)": 0.90,
        "chicken breast": 0.99,
        "beef (ground)": 0.90,
        "pasta (uncooked)": 0.68,
        "rice (uncooked)": 0.68,
        "chocolate chips": 0.55,
        "vanilla extract": 1.03,
        "cocoa powder": 0.86
    } # to be expend

    def metric_dict(self):
        return self.__metric_dict

    def imperial_vol_dict(self):
        return self.__imperial_vol_dict

    def imperial_mass_dict(self):
        return self.__imperial_mass_dict

    def cup_by_country_dict(self):
        return self.__cup_by_country_dict

    def teaspoon_by_country_dict(self):
        return self.__teaspoon_by_country_dict

    def tablespoon_by_country_dict(self):
        return self.__tablespoon_by_country_dict

    def ml_to_g_by_ingredient_dict(self):
        return self.__ml_to_g_by_ingredient_dict



# UNITS list, all the values should be lower case
UNITS = [
    {
        "name": "weight",
        "units": [
            {"name": "gram", "si": "g"}, #metric
            {"name": "kilogram", "si": "kg"},
            {"name": "milligram", "si": "mg"},
            {"name": "ounce", "si": "oz"}, #imperial
            {"name": "pound", "si": "lb"},
            {"name": "ton", "si": "t"},
            {"name": "hundredweight", "si": "cwt"},
            {"name": "quarter", "si": "qr"},
            {"name": "stone", "si": "st"},
            {"name": "dram", "si": "dr"},
            {"name": "grain", "si": "gr"}
        ]
    },
    {
        "name": "volume",
        "units": [
            {"name": "liter", "si": "l"}, #metric
            {"name": "milliliter", "si": "ml"},
            {"name": "gallon", "si": "gal"}, #imperial
            {"name": "quart", "si": "qt"},
            {"name": "pint", "si": "pt"},
            {"name": "gill", "si": "gi"},
            {"name": "fluid ounce", "si": "fl oz"},
            {"name": "fluid oz", "si": "fl oz"},
            {"name": "fl ounce", "si": "fl oz"},
            {"name": "teaspoon", "si": "tsp"}, #other
            {"name": "tablespoon", "si": "tbsp"},
            {"name": "cup", "si": None}
        ]
    },
    {
        "name": "distance",
        "units": [
            {"name": "millimeter", "si": "mm"},
            {"name": "centimeter", "si": "cm"},
            {"name": "inch", "si": "in"}
        ]
    },
    {
        "name": "other",
        "units": [
            {"name": "slice", "si": None},
            {"name": "whole", "si": None},
            {"name": "dozen", "si": None},
            {"name": "pinch", "si": None},
            {"name": "dash", "si": None},
            {"name": "drop", "si": None},
            {"name": "sprinkle", "si": None},
            {"name": "handful", "si": None},
            {"name": "bunch", "si": None},
            {"name": "head", "si": None},
            {"name": "clove", "si": None},
            {"name": "fillet", "si": None},
            {"name": "portion", "si": None},
            {"name": "serving", "si": None},
            {"name": "piece", "si": None},
            {"name": "packet", "si": None},
            {"name": "can", "si": None},
            {"name": "jar", "si": None},
            {"name": "bottle", "si": None}
        ]
    }
]

Convert_Dict=Dictionary()
