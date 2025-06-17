import json
from itertools import product

from app.domain_services import get_typology_instance


def main(output_path="mock_users.json"):
    socionics = get_typology_instance("Socionics")
    psychosophy = get_typology_instance("Psychosophia")
    temporistics = get_typology_instance("Temporistics")

    # Convert any lazy translation strings to plain strings for JSON serialization
    soc_types = [str(t) for t in socionics.get_all_types()]
    psych_types = [str(t) for t in psychosophy.get_all_types()]
    temp_types = [str(t) for t in temporistics.get_all_types()]

    users = []
    index = 1
    for soc, psych, temp in product(soc_types, psych_types, temp_types):
        users.append({
            "username": f"user_{index}",
            "email": f"user_{index}@example.com",
            "socionics": soc,
            "psychosophy": psych,
            "temporistics": temp,
        })
        index += 1

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(users)} mock users in {output_path}")


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "mock_users.json"
    main(path)
