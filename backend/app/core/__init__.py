"""
Core module initialization file for the GrubTrack backend application.
This module contains core functionality and configurations for the application.
"""

from pathlib import Path

# Define base directories
ROOT_DIR = Path(__file__).parent.parent.parent
APP_DIR = Path(__file__).parent.parent

# Version information
__version__ = "1.0.0"

# Initialize core module components
from .config import settings  # noqa: F401
from .security import get_password_hash, verify_password  # noqa: F401
from .database import Base, get_db  # noqa: F401

# Export commonly used components
__all__ = [
    "settings",
    "get_password_hash",
    "verify_password",
    "Base",
    "get_db",
]