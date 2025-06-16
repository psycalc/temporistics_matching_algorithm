import json
import shutil
import subprocess
from pathlib import Path
from app import statistics_utils as su


def test_adjust_comfort_score_script(tmp_path, monkeypatch):
    src = su.get_data_path("psychosophia_comfort_scores.json")
    dest = tmp_path / "psychosophia_comfort_scores.json"
    shutil.copy(src, dest)

    script = Path("adjust_comfort_score.py")
    result = subprocess.run(
        ["python", str(script), "Psychosophia", "Identity/Philia", "77", "--data-dir", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    with open(dest) as f:
        data = json.load(f)
    assert data["Identity/Philia"]["score"] == 77
