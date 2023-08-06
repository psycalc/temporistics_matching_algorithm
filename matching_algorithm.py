from itertools import permutations

class TypologyAspect:
    def __init__(self, aspect_name: str, position: int):
        self.aspect_name = aspect_name
        self.position = position

    def __str__(self):
        return self.aspect_name

class Typology:
    def __init__(self, aspects: list[str]):
        self.aspects = [TypologyAspect(name, index) for index, name in enumerate(aspects, 1)]

    def get_all_types(self):
        # Get all permutations of aspects
        for aspect_set in [list(perm) for perm in permutations(self.aspects)]:
               print(", ".join(map(str, aspect_set))) 

class TypologyPsychosophia(Typology):
    def __init__(self):
        super().__init__(["Emotion", "Logic", "Will", "Power"])

class TypologySocionics(Typology):
    def __init__(self):
        super().__init__(["Ethics", "Logic", "Sensation", "Intuition"])
    # we should override the get_all_types method for socionics
    # becase the there no Intuite and Sensation for the same person
    # person can be Intuitive or Sensation not both
    def get_all_types(self):
        # Get all permutations of aspects
        for aspect_set in [list(perm) for perm in permutations(self.aspects)]:
            if aspect_set[2].aspect_name == "Sensation" and aspect_set[3].aspect_name == "Intuition":
                continue
            elif aspect_set[2].aspect_name == "Intuition" and aspect_set[3].aspect_name == "Sensation":
                continue
            else:
                print(", ".join(map(str, aspect_set)))

class TypologyTemporistics(Typology):
    def __init__(self):
        super().__init__(["Past", "Present", "Future", "Eternity"])

# example of usage
typology = TypologyPsychosophia()

# Print each aspect set on a new line
typology.get_all_types()


typology = TypologySocionics()

# Print each aspect set on a new line
typology.get_all_types().count()

typology = TypologyTemporistics()

# Print each aspect set on a new line
typology.get_all_types()

