#!/usr/bin/env python3
"""
Module: ui.py

Provides the settings window for the Battery Monitor application.
"""

import tkinter as tk
from tkinter import ttk
import time

# Global configuration variables.
battery_threshold = 20      # Battery threshold percentage
check_interval = 60         # Interval between battery checks (in seconds)
checker_enabled = True      # Whether the battery checker is active
disable_duration = "None"   # Options: "None", "1 hour", "8 hours", "1 day", "Until I turn it back on"
disable_until = None        # Timestamp when the disable period expires (or None)

def show_settings():
    global battery_threshold, check_interval, checker_enabled, disable_duration, disable_until

    root = tk.Tk()
    root.title("Battery Monitor Settings")

    # --- Battery Threshold Slider ---
    threshold_frame = tk.Frame(root)
    threshold_frame.pack(pady=5, padx=10, fill="x")
    tk.Label(threshold_frame, text="Battery Threshold (%):").pack(anchor="w")
    threshold_label = tk.Label(threshold_frame, text=f"{battery_threshold}%")
    threshold_label.pack(anchor="w")

    def update_threshold(value):
        global battery_threshold
        battery_threshold = int(value)
        threshold_label.config(text=f"{battery_threshold}%")

    threshold_slider = tk.Scale(threshold_frame, from_=0, to=100,
                                orient=tk.HORIZONTAL, command=update_threshold)
    threshold_slider.set(battery_threshold)
    threshold_slider.pack(fill="x")

    # --- Check Interval Slider ---
    interval_frame = tk.Frame(root)
    interval_frame.pack(pady=5, padx=10, fill="x")
    tk.Label(interval_frame, text="Check Interval (seconds):").pack(anchor="w")
    interval_label = tk.Label(interval_frame, text=f"{check_interval}")
    interval_label.pack(anchor="w")

    def update_interval(value):
        global check_interval
        check_interval = int(value)
        interval_label.config(text=f"{check_interval}")

    interval_slider = tk.Scale(interval_frame, from_=10, to=600,
                               orient=tk.HORIZONTAL, command=update_interval)
    interval_slider.set(check_interval)
    interval_slider.pack(fill="x")

    # --- Enable/Disable Checker Toggle ---
    toggle_frame = tk.Frame(root)
    toggle_frame.pack(pady=5, padx=10, fill="x")

    def toggle_checker():
        global checker_enabled
        checker_enabled = not checker_enabled
        status_label.config(text=f"Checker is {'Enabled' if checker_enabled else 'Disabled'}")

    toggle_btn = tk.Button(toggle_frame, text="Toggle Checker", command=toggle_checker)
    toggle_btn.pack(anchor="w")
    status_label = tk.Label(toggle_frame, text=f"Checker is {'Enabled' if checker_enabled else 'Disabled'}")
    status_label.pack(anchor="w")

    # --- Disable Duration Option Menu with Countdown ---
    duration_frame = tk.Frame(root)
    duration_frame.pack(pady=5, padx=10, fill="x")
    duration_label = tk.Label(duration_frame, text="Disable Power Monitor:").pack(anchor="w")
    duration_options = ["None", "1 hour", "8 hours", "1 day", "Until I turn it back on"]
    disable_var = tk.StringVar(root, value=disable_duration)
    # Mapping timed options to seconds.
    duration_seconds = {"1 hour": 3600, "8 hours": 8 * 3600, "1 day": 24 * 3600}

    # Label to display remaining time.
    time_left_label = tk.Label(duration_frame, text="")
    time_left_label.pack(anchor="w")

    # --- Define update_time_left before it is used ---
    def update_time_left():
        """
        Updates the remaining time label based on disable_until.
        Enables the Reset button only if a timed disable is active and time remains.
        """
        if disable_duration in duration_seconds and disable_until is not None:
            remaining = disable_until - time.time()
            if remaining > 0:
                hours_left = int(remaining // 3600)
                duration_label.config(text=f"({hours_left} hour{'s' if hours_left != 1 else ''} left)")
                reset_btn.config(state="normal")
            else:
                disable_var.set("None")
                reset_btn.config(state="disabled")
                time_left_label.config(text="")
        else:
            time_left_label.config(text="")
            reset_btn.config(state="disabled")
        # Schedule next update in one minute.
        root.after(60000, update_time_left)

    def update_disable_duration(*args):
        """
        Updates the disable_duration setting and sets the expiration timestamp if needed.
        """
        global disable_duration, disable_until
        disable_duration = disable_var.get()
        if disable_duration in duration_seconds:
            disable_until = time.time() + duration_seconds[disable_duration]
        else:
            disable_until = None
        update_time_left()

    disable_var.trace("w", update_disable_duration)
    duration_menu = ttk.OptionMenu(duration_frame, disable_var, disable_duration, *duration_options)
    duration_menu.pack(anchor="w")

    # Reset button to cancel the disable period.
    reset_btn = tk.Button(duration_frame, text="Reset", command=lambda: disable_var.set("None"))
    reset_btn.pack(anchor="w")

    # Initialize the time left display.
    update_time_left()

    # --- Close Button ---
    close_btn = tk.Button(root, text="Close", command=root.destroy)
    close_btn.pack(pady=10)

    root.mainloop()

def get_settings():
    """
    Returns the current settings as a dictionary.
    """
    return {
        "battery_threshold": battery_threshold,
        "check_interval": check_interval,
        "checker_enabled": checker_enabled,
        "disable_duration": disable_duration,
        "disable_until": disable_until
    }

if __name__ == '__main__':
    show_settings()
