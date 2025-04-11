#!/usr/bin/env python3
"""
Module: tray.py

A Tray class to create and configure the system tray icon.
"""
from __future__ import annotations

from pystray import Icon, Menu, MenuItem
import PIL.Image
from config import ASSETS_DIR, BATTERY_THRESHOLD_OPTIONS

from utils import resource_path

class Tray:
    def __init__(self, app_config):
        self.app_config = app_config

        # Load the tray icon images
        self.enabled_icon = PIL.Image.open(resource_path(ASSETS_DIR / "green-battery-128.ico"))
        self.disabled_icon = PIL.Image.open(resource_path(ASSETS_DIR / "orange-battery-128.ico"))
        self.error_icon = PIL.Image.open(resource_path(ASSETS_DIR / "red-battery-128.ico"))

        # Build the tray menu with a toggle item
        menu = Menu(
            MenuItem(
                f"Active: {self.app_config.battery_threshold}%",
                Menu(
                    MenuItem(
                        f"{BATTERY_THRESHOLD_OPTIONS[0]}%",
                        lambda icon, item: self.toggle_power_monitor(icon, BATTERY_THRESHOLD_OPTIONS[0])),
                    MenuItem(
                        f"{BATTERY_THRESHOLD_OPTIONS[1]}%",
                        lambda icon, item: self.toggle_power_monitor(icon, BATTERY_THRESHOLD_OPTIONS[1])),
                    MenuItem(
                        f"{BATTERY_THRESHOLD_OPTIONS[2]}%",
                        lambda icon, item: self.toggle_power_monitor(icon, BATTERY_THRESHOLD_OPTIONS[2])),
                    MenuItem(
                        "Disable",
                        lambda icon, item: self.toggle_power_monitor(icon, None)),
                )),
            MenuItem("Exit", self.on_exit)
        )

        # Create the Icon instance
        self.icon = Icon("Battery Monitor", self.enabled_icon, menu=menu)

    def set_error(self, icon: Icon, error_msg):
        icon = self.error_icon
        icon.menu = Menu(
            MenuItem(
                error_msg,
                lambda icon, item: 1
            )
        )

    def toggle_power_monitor(self, icon: Icon, selected_battery_threshold: int | None):
        """Toggle the battery monitor's disabled state."""
        if selected_battery_threshold in BATTERY_THRESHOLD_OPTIONS:
            self.app_config.enabled = True
            self.app_config.battery_threshold = selected_battery_threshold
            icon.icon = self.enabled_icon
            menu_label = f"Active: {self.app_config.battery_threshold}%"
        elif selected_battery_threshold is None:
            self.app_config.enabled = False
            icon.icon = self.disabled_icon
            menu_label = "Enable"
        else:
            raise ValueError(f"Invalid battery threshold selected: '{selected_battery_threshold}'")
        icon.menu = Menu(
            MenuItem(
                menu_label,
                Menu(
                    MenuItem(
                        f"{BATTERY_THRESHOLD_OPTIONS[0]}%",
                        lambda icon, item: self.toggle_power_monitor(icon, BATTERY_THRESHOLD_OPTIONS[0])),
                    MenuItem(
                        f"{BATTERY_THRESHOLD_OPTIONS[1]}%",
                        lambda icon, item: self.toggle_power_monitor(icon, BATTERY_THRESHOLD_OPTIONS[1])),
                    MenuItem(
                        f"{BATTERY_THRESHOLD_OPTIONS[2]}%",
                        lambda icon, item: self.toggle_power_monitor(icon, BATTERY_THRESHOLD_OPTIONS[2])),
                    MenuItem(
                        "Disable",
                        lambda icon, item: self.toggle_power_monitor(icon, None)),
                )),
            MenuItem("Exit", self.on_exit)
        )

    def on_exit(self, icon, item):
        icon.stop()

    def run(self):
        self.icon.run()
