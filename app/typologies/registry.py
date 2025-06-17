# app/typologies/registry.py
"""Registry and plugin loader for typology classes."""
from __future__ import annotations
import importlib
from typing import Dict, Type
from stevedore import extension

_typology_registry: Dict[str, Type] = {}


def register_typology(name: str, cls: Type) -> None:
    """Register a typology class under the given name."""
    _typology_registry[name] = cls


def get_typology_classes() -> Dict[str, Type]:
    """Return a mapping of registered typology names to their classes."""
    return _typology_registry


def load_plugins() -> None:
    """Load typology plugins registered via ``stevedore`` entry points.

    Packages can expose entry points under the ``temporistics.typology``
    namespace. Each plugin module should call :func:`register_typology` to
    register its classes when imported.
    """
    manager = extension.ExtensionManager(
        namespace="temporistics.typology",
        invoke_on_load=False,
    )
    for ext in manager:
        importlib.import_module(ext.entry_point.module_name)


# Automatically load any plugins when the registry module is imported
load_plugins()
