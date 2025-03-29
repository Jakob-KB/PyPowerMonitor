#! /usr/bin/env python3

from pystray import Icon, Menu, MenuItem
import PIL.Image
from config.config import ASSETS_DIR

# Define the image path and create a PIL Image object
image_path = ASSETS_DIR / "battery-128.ico"
image = PIL.Image.open(image_path)

def on_clicked(icon):
    """
    Called when the menu is clicked.
    Triggers a system notification.
    """
    icon.notify("Hello World!", "Test Notification")

# Create and run the actual tray icon
tray_icon = Icon(
    "test",
    icon=image,
    menu=Menu(MenuItem("Click me!", on_clicked))
)
tray_icon.run()
