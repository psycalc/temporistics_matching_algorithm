from flask_caching import Cache
from .typologies import TypologyTemporistics, TypologyPsychosophia, TypologyAmatoric, TypologySocionics

cache = Cache()  # Initialize Cache without passing the app instance

@cache.memoize(timeout=3600)  # Cache the result for 1 hour
def get_types_by_typology(typology_name):
    typology_classes = {
        "Temporistics": TypologyTemporistics,
        "Psychosophia": TypologyPsychosophia,
        "Amatoric": TypologyAmatoric,
        "Socionics": TypologySocionics
    }
    typology_class = typology_classes.get(typology_name)
    if not typology_class:
        return None
    return typology_class().get_all_types()