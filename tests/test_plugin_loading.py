import types
import sys
from pathlib import Path
from app.typologies import registry
from stevedore import extension


def test_load_plugins_with_stevedore(monkeypatch, tmp_path):
    """Ensure plugins discovered via stevedore register their typology."""
    # Write a temporary plugin module
    plugin_file = tmp_path / "dummy_typology.py"
    plugin_file.write_text(
        "from app.typologies.registry import register_typology\n"
        "class DummyTypology:\n    pass\n"
        "register_typology('Dummy', DummyTypology)\n"
    )
    sys.path.insert(0, str(tmp_path))

    # Ensure built-in typologies are loaded before snapshotting
    import importlib
    importlib.import_module("app.typologies.typology_temporistics")
    importlib.import_module("app.typologies.typology_psychosophia")
    importlib.import_module("app.typologies.typology_amatoric")
    importlib.import_module("app.typologies.typology_socionics")
    importlib.import_module("app.typologies.typology_iq")
    importlib.import_module("app.typologies.typology_temperaments")

    class DummyExt:
        def __init__(self, module_name):
            self.entry_point = types.SimpleNamespace(module_name=module_name)

    class DummyManager:
        def __init__(self, *a, **k):
            self.extensions = [DummyExt("dummy_typology")]

        def __iter__(self):
            return iter(self.extensions)

    monkeypatch.setattr(extension, "ExtensionManager", DummyManager)

    original = registry._typology_registry.copy()
    registry._typology_registry.clear()
    registry.load_plugins()

    assert "Dummy" in registry.get_typology_classes()

    registry._typology_registry.clear()
    registry._typology_registry.update(original)
    sys.path.remove(str(tmp_path))
