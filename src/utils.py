#!/usr/bin/env python3
"""
Module: tray.py

A Tray class to create and configure the system tray icon.
"""

import sys
import os
from pathlib import Path

def resource_path(relative_path):
    """
    Get absolute path to resource, works for development and for PyInstaller EXE.
    """
    try:
        # PyInstaller created attribute
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("")
    return Path(base_path) / relative_path
