#!/usr/bin/env python3
"""
Module: tray.py

Provides a Tray class to create and configure the system tray icon.
"""

from pystray import Icon, Menu, MenuItem
import PIL.Image
from config.config import ASSETS_DIR
from ui import AppUI

class Tray:
    def __init__(self, app_config):
        self.app_config = app_config

        # Load the tray icon image.
        image_path = ASSETS_DIR / "battery-128.ico"
        image = PIL.Image.open(image_path)

        # Build the tray menu.
        menu = Menu(
            MenuItem("Settings", self.launch_ui),
            MenuItem("Exit", self.on_exit)
        )

        # Create the Icon instance.
        self.icon = Icon("Battery Monitor", image, menu=menu)
        # Bind left-click to open the settings window.
        self.icon.on_clicked = self.launch_ui

    def launch_ui(self, icon, item):
        """
        Callback to open the settings window.
        Instantiates the AppUI with the current app_config.
        """
        ui = AppUI(self.app_config)
        ui.show()

    def on_exit(self, icon, item):
        """
        Callback to exit the application.
        """
        icon.stop()

    def run(self):
        """
        Starts the tray icon's event loop.
        """
        self.icon.run()
