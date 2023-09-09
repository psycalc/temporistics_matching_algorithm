

from typology_temporistics import TypologyTemporistics
from typology_psychosophia import TypologyPsychosophia
from typology_amatoric import TypologyAmatoric
from typology_socionics import TypologySocionics

class RelationshipCalculator:
    """A class to calculate the relationship type and comfort score between two users based on their typology aspects."""
    


    # Relationship types
    RELATIONSHIP_PHILIA = "Philia"
    RELATIONSHIP_PSEUDO_PHILIA = "Pseudo-Philia"
    RELATIONSHIP_AGAPE = "Agape"
    RELATIONSHIP_FULL_AGAPE = "Full Agape"
    RELATIONSHIP_EROS = "Eros"
    RELATIONSHIP_EROS_VARIANT = "Eros Variant"
    RELATIONSHIP_FULL_EROS = "Full Eros"
    
    # Comfort scores for each relationship type
    COMFORT_SCORES = {
        RELATIONSHIP_PHILIA: 5,
        RELATIONSHIP_PSEUDO_PHILIA: 3,
        RELATIONSHIP_AGAPE: 8,
        RELATIONSHIP_FULL_AGAPE: 10,
        RELATIONSHIP_EROS: -2,
        RELATIONSHIP_EROS_VARIANT: -1,
        RELATIONSHIP_FULL_EROS: -5
    }

        # Terminal color codes
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

    # ... [rest of your class definition remains unchanged]

    def get_relationship_color(self, comfort_score):
        """Return the color code based on comfort score."""
        if comfort_score > 0:
            return self.GREEN
        elif comfort_score < 0:
            return self.RED
        else:
            return self.YELLOW

    def __init__(self, user1, user2, typology):
        """Initialize the class with two users."""
        self.user1 = user1
        self.user2 = user2
        self.typology = typology

    def determine_relationship_type(self):
        """Determine the type of relationship between the two users."""
        if self.user1 == self.user2:
            return self.RELATIONSHIP_PHILIA
        
        # Logic for Pseudo-Philia
        if (
            (self.user1[0] == self.user2[0] and self.user1[3] == self.user2[3]) or
            (self.user1[1] == self.user2[1] and self.user1[2] == self.user2[2])
        ):
            return self.RELATIONSHIP_PSEUDO_PHILIA
        
        if (
            (self.user1[1] == self.user2[2] and self.user1[2] == self.user2[1]) and 
            (self.user1[0] == self.user2[3] and self.user1[3] == self.user2[0])
        ):
            return self.RELATIONSHIP_FULL_AGAPE

        if self.user1[0] == self.user2[0] and self.user1[1] == self.user2[2]:
            return self.RELATIONSHIP_AGAPE
            
        if (
            (self.user1[0] == self.user2[2] or self.user1[2] == self.user2[0]) and
            (self.user1[1] == self.user2[3] or self.user1[3] == self.user2[1])
        ):
            return self.RELATIONSHIP_FULL_EROS

        if self.user1[0] == self.user2[2] or self.user1[2] == self.user2[0]:
            return self.RELATIONSHIP_EROS

        if self.user1[1] == self.user2[3] or self.user1[3] == self.user2[1]:
            return self.RELATIONSHIP_EROS_VARIANT

        return "Unknown Relationship"


    def get_comfort_score(self, relationship_type):
        """Return the comfort score for the given relationship type."""
        return self.COMFORT_SCORES.get(relationship_type, 0)  # Default to 0 if relationship type is not found
    

# create an instance of the RelationshipCalculator class
temporitics = TypologyTemporistics()
# show all types
print(temporitics.get_all_types())
psychosophia = TypologyPsychosophia()
# show all types
print(psychosophia.get_all_types())
amatoric = TypologyAmatoric()
# show all types
print(amatoric.get_all_types())
socionics = TypologySocionics()
# show all types
print(socionics.get_all_types())


