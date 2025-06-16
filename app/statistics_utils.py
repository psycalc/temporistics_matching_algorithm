import json
import os
from typing import Dict

from .services import calculate_relationship

BASE_DIR = os.environ.get(
    "DATA_DIR",
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data"),
)
WEIGHTS_FILE = os.environ.get("WEIGHTS_FILE", os.path.join(BASE_DIR, "typology_weights.json"))
STATUS_FILE = os.environ.get("STATUS_FILE", os.path.join(BASE_DIR, "typology_status.json"))


def get_data_path(filename: str) -> str:
    return os.path.join(BASE_DIR, filename)


def load_typology_weights() -> Dict[str, float]:
    if not os.path.exists(WEIGHTS_FILE):
        weights = {
            "Temporistics": 1.0,
            "Psychosophia": 1.0,
            "Amatoric": 1.0,
            "Socionics": 1.0,
            "IQ": 1.0,
        }
        with open(WEIGHTS_FILE, "w") as f:
            json.dump(weights, f, indent=2)
        return weights
    with open(WEIGHTS_FILE) as f:
        return json.load(f)


def update_typology_weight(typology_name: str, new_weight: float) -> None:
    weights = load_typology_weights()
    weights[typology_name] = new_weight
    with open(WEIGHTS_FILE, "w") as f:
        json.dump(weights, f, indent=2)


def load_typology_status() -> Dict[str, bool]:
    if not os.path.exists(STATUS_FILE):
        status = {
            "Temporistics": True,
            "Psychosophia": True,
            "Amatoric": True,
            "Socionics": True,
            "IQ": True,
        }
        with open(STATUS_FILE, "w") as f:
            json.dump(status, f, indent=2)
        return status
    with open(STATUS_FILE) as f:
        return json.load(f)


def update_typology_status(typology_name: str, enabled: bool) -> None:
    status = load_typology_status()
    status[typology_name] = enabled
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2)


def update_comfort_score(typology_name: str, relationship_type: str, new_score: int) -> None:
    file_map = {
        "Temporistics": "temporistics_comfort_scores.json",
        "Psychosophia": "psychosophia_comfort_scores.json",
        "Socionics": "socionics_relationships.json",
        "Amatoric": "amatoric_comfort_scores.json",
    }
    filename = file_map.get(typology_name)
    if not filename:
        raise ValueError(f"Unknown typology {typology_name}")
    path = get_data_path(filename)
    with open(path) as f:
        data = json.load(f)
    entry = data.get(relationship_type, {})
    if isinstance(entry, dict):
        entry["score"] = new_score
    else:
        entry = {"score": new_score, "description": ""}
    data[relationship_type] = entry
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def calculate_weighted_compatibility(
    user1_types: Dict[str, str], user2_types: Dict[str, str], weights: Dict[str, float] | None = None
) -> float:
    if weights is None:
        weights = load_typology_weights()
    total_weight = 0.0
    weighted_score = 0.0
    for typology, weight in weights.items():
        t1 = user1_types.get(typology)
        t2 = user2_types.get(typology)
        if not t1 or not t2:
            continue
        _, score = calculate_relationship(t1, t2, typology)
        weighted_score += score * weight
        total_weight += weight
    if total_weight == 0:
        raise ValueError("No valid typologies for calculation")
    return weighted_score / total_weight
