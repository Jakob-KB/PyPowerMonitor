#!/usr/bin/env python3
"""
Module: ui.py

Provides a minimal AppUI class for the Battery Monitor application.
It displays a settings window that reflects the current AppConfig
and lets the user update the disable duration.
"""

import tkinter as tk
from tkinter import ttk
import time

UI_POLLING_INTERVAL = 1000

class AppUI:
    def __init__(self, app_config):
        self.app_config = app_config
        self.duration_options = ["None", "1 hour", "8 hours", "1 day", "Until I turn it back on"]

    def show(self):
        root = tk.Tk()
        root.title("Battery Monitor Settings")

        # --- Disable Duration Option ---
        frame = tk.Frame(root)
        frame.pack(pady=10, padx=10, fill="x")

        # Label showing the current disable duration from the app config.
        disable_label = tk.Label(frame, text="Disable Power Monitor:").pack(anchor="w")

        # Use the current config value to initialize the dropdown.
        disable_var = tk.StringVar(root, value=self.app_config.set_disable_duration)

        # Callback: when the dropdown value changes, simply update the app config.
        def on_duration_change(*args):
            self.app_config.set_disable_duration = disable_var.get()

        def update_time_left(*args):
            if self.app_config.is_disabled == True:
                remaining = self.app_config.disabled_until - time.time()
                if remaining > 0:
                    # In testing mode, each second represents one "hour".
                    hours_left = int(remaining)
                    disable_label.config(
                        text=f"Disable Power Monitor ({hours_left} hour{'s' if hours_left != 1 else ''} left):")

        root.after(UI_POLLING_INTERVAL, update_time_left)


        disable_var.trace("w", on_duration_change)

        # Dropdown menu for selecting the disable duration.
        dropdown = ttk.OptionMenu(frame, disable_var, self.app_config.set_disable_duration, *self.duration_options)
        dropdown.pack(anchor="w", pady=(5, 0))

        # Close button to exit the settings window.
        close_btn = tk.Button(root, text="Save & Close", command=root.destroy)
        close_btn.pack(pady=10)

        root.mainloop()
