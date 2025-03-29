#!/usr/bin/env python3
"""
Module: tray.py

Provides functionality to create and configure the system tray icon.
Left-click opens the settings window.
"""

from pystray import Icon, Menu, MenuItem
import PIL.Image
from config.config import ASSETS_DIR
from ui import show_settings

def on_clicked(icon, item):
    """
    Callback invoked when the tray menu's "Test Notification" item is clicked.
    Triggers a system notification.
    """
    icon.notify("Hello World!", "Test Notification")

def on_settings(icon, item):
    """
    Callback to open the settings window.
    """
    show_settings()

def on_exit(icon, item):
    """
    Callback to exit the application.
    """
    icon.stop()

def create_tray_icon() -> Icon:
    """
    Creates and configures the system tray icon.

    :returns: An Icon instance with the loaded image and configured menu.
    """
    image_path = ASSETS_DIR / "battery-128.ico"
    image = PIL.Image.open(image_path)
    menu = Menu(
        MenuItem("Test Notification", on_clicked),
        MenuItem("Settings", on_settings),
        MenuItem("Exit", on_exit)
    )
    tray_icon = Icon("Battery Monitor", image, menu=menu)
    # Attempt to assign left-click to open settings (behavior may vary by platform).
    tray_icon.on_clicked = on_settings
    return tray_icon

if __name__ == '__main__':
    tray_icon = create_tray_icon()
    tray_icon.run()
