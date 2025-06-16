# app/typologies/registry.py
"""Registry and plugin loader for typology classes."""
from __future__ import annotations
import os
import importlib
from typing import Dict, Type

_typology_registry: Dict[str, Type] = {}


def register_typology(name: str, cls: Type) -> None:
    """Register a typology class under the given name."""
    _typology_registry[name] = cls


def get_typology_classes() -> Dict[str, Type]:
    """Return a mapping of registered typology names to their classes."""
    return _typology_registry


def load_plugins() -> None:
    """Import extra typology modules listed in ``TYPOLOGY_PLUGINS`` env var."""
    plugins = os.environ.get("TYPOLOGY_PLUGINS", "")
    for module_name in [m.strip() for m in plugins.split(",") if m.strip()]:
        importlib.import_module(module_name)


# Automatically load any plugins when the registry module is imported
load_plugins()
