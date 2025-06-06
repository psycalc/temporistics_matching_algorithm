import importlib
import json

import app.statistics_utils as su


def test_load_typology_weights_creates_file(tmp_path, monkeypatch):
    weights_file = tmp_path / "weights.json"
    monkeypatch.setenv("WEIGHTS_FILE", str(weights_file))
    importlib.reload(su)
    weights = su.load_typology_weights()
    assert weights["Temporistics"] == 1.0
    assert weights_file.exists()


def test_update_typology_weight(tmp_path, monkeypatch):
    weights_file = tmp_path / "weights.json"
    monkeypatch.setenv("WEIGHTS_FILE", str(weights_file))
    importlib.reload(su)
    su.load_typology_weights()
    su.update_typology_weight("Temporistics", 2.0)
    with open(weights_file) as f:
        data = json.load(f)
    assert data["Temporistics"] == 2.0


def test_update_comfort_score(tmp_path, monkeypatch):
    src = su.get_data_path("psychosophia_comfort_scores.json")
    dest_dir = tmp_path
    dest = dest_dir / "psychosophia_comfort_scores.json"
    monkeypatch.setenv("DATA_DIR", str(dest_dir))
    importlib.reload(su)
    import shutil

    shutil.copy(src, dest)
    su.update_comfort_score("Psychosophia", "Identity/Philia", 99)
    with open(dest) as f:
        data = json.load(f)
    assert data["Identity/Philia"]["score"] == 99


def test_calculate_weighted_compatibility(tmp_path, monkeypatch):
    weights_file = tmp_path / "weights.json"
    monkeypatch.setenv("WEIGHTS_FILE", str(weights_file))
    importlib.reload(su)
    su.load_typology_weights()  # create default
    user1 = {"Temporistics": "Past, Current, Future, Eternity"}
    user2 = {"Temporistics": "Past, Current, Future, Eternity"}
    score = su.calculate_weighted_compatibility(user1, user2)
    assert score == 95


def test_load_typology_status_creates_file(tmp_path, monkeypatch):
    status_file = tmp_path / "status.json"
    monkeypatch.setenv("STATUS_FILE", str(status_file))
    importlib.reload(su)
    status = su.load_typology_status()
    assert status["Temporistics"] is True
    assert status_file.exists()


def test_update_typology_status(tmp_path, monkeypatch):
    status_file = tmp_path / "status.json"
    monkeypatch.setenv("STATUS_FILE", str(status_file))
    importlib.reload(su)
    su.load_typology_status()
    su.update_typology_status("Temporistics", False)
    with open(status_file) as f:
        data = json.load(f)
    assert data["Temporistics"] is False
