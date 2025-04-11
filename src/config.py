#!/usr/bin/env python3
"""
Module: config.py

Stores default settings and filepaths.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
ASSETS_DIR = PROJECT_ROOT / "assets"


DEFAULT_BATTERY_THRESHOLD = 10

DEFAULT_QUERY_INTERVAL = 10
ALERT_QUERY_INTERVAL = 5

BATTERY_THRESHOLD_OPTIONS = [5, 8, 10, 15, 95]
