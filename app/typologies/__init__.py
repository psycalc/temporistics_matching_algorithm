# app/typologies/__init__.py
"""
Initializes the typologies package and makes its modules available for import elsewhere in the application.
This allows for a cleaner import syntax and organizes the code related to different typology classes.
"""

# Import the typology classes to make them available when importing the package
from .typology_temporistics import TypologyTemporistics
from .typology_psychosophia import TypologyPsychosophia
from .typology_amatoric import TypologyAmatoric
from .typology_socionics import TypologySocionics

# List all the classes that should be available when importing the package
__all__ = [
    "TypologyTemporistics",
    "TypologyPsychosophia",
    "TypologyAmatoric",
    "TypologySocionics",
]

# This allows the classes to be imported directly from the package
# Example: from app.typologies import TypologyTemporistics
