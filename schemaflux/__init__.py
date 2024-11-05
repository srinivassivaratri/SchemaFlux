"""
A lightweight PostgreSQL migration library.
"""
from .core import MigrationManager
from .cli import cli

__version__ = "1.0.0"
__all__ = ["MigrationManager", "cli"]
