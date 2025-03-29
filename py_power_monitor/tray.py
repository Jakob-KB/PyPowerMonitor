#!/usr/bin/env python3
"""
Module: tray.py

A Tray class to create and configure the system tray icon.
"""

from pystray import Icon, Menu, MenuItem
import PIL.Image
from config.config import ASSETS_DIR


class Tray:
    def __init__(self, app_config):
        self.app_config = app_config

        # Load the tray icon images
        enabled_image_path = ASSETS_DIR / "green-battery-128.ico"
        self.enabled_image = PIL.Image.open(enabled_image_path)

        disabled_image_path = ASSETS_DIR / "red-battery-128.ico"
        self.disabled_image = PIL.Image.open(disabled_image_path)

        # Build the tray menu with a toggle item
        menu = Menu(
            MenuItem("Disable", self.toggle_power_monitor),
            MenuItem("Exit", self.on_exit)
        )

        # Create the Icon instance
        self.icon = Icon("Battery Monitor", self.enabled_image, menu=menu)


    def toggle_power_monitor(self, icon, item):
        """Toggle the battery monitor's disabled state."""
        if self.app_config.is_disabled:
            # Enable the monitor
            self.app_config.is_disabled = False
            icon.icon = self.enabled_image
            new_label = "Disable"
        else:
            # Disable the monitor
            self.app_config.is_disabled = True
            icon.icon = self.disabled_image
            new_label = "Enable"

        # Recreate the menu with the updated toggle label
        icon.menu = Menu(
            MenuItem(new_label, self.toggle_power_monitor),
            MenuItem("Exit", self.on_exit)
        )

    def on_exit(self, icon, item):
        icon.stop()

    def run(self):
        self.icon.run()
