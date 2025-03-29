#!/usr/bin/env python3
"""
Module: main.py

Entry point for the application. This module defines an Application class that holds
the current settings, app state (like disable time left), and methods to start the battery
monitor, tray icon, and to load/save configuration from/to a JSON file.
"""

import threading
import time
import json
from battery import get_system_power_status
from tray import Tray
from dataclasses import dataclass


# noinspection PyCompatibility
@dataclass
class AppConfig:
    battery_threshold: int
    battery_query_interval: int
    set_disable_duration: str = "None"
    disabled_until: float = -1
    is_disabled: bool = False

    def to_dict(self):
        """
        Returns a dictionary containing only the persistent settings.
        """
        return {
            "battery_threshold": self.battery_threshold,
            "battery_query_interval": self.battery_query_interval
        }

disable_time_mapping = {
    "None": 0,
    "1 hour": 3600,
    "8 hours": 3600 * 8,
    "1 day": 3600 * 24,
    "Until I turn it back on": -1
}

disable_duration_options = ["None", "1 hour", "8 hours", "1 day", "Until I turn it back on"]



# noinspection PyCompatibility
class Application:
    app_config: AppConfig

    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.load_config()

        # Create the tray icon using the Tray class, passing the settings
        self.tray_icon = Tray(self.app_config)
        self.monitor_thread = threading.Thread(
            target=self.battery_monitor, daemon=True
        )

    def battery_monitor(self):
        while True:
            try:
                print(self.app_config)
                # Check if the monitor is disabled
                if self.app_config.set_disable_duration not in disable_duration_options:
                    raise Exception("Invalid disable duration option.")

                if self.app_config.set_disable_duration == "None":
                    self.app_config.is_disabled = False
                    self.app_config.disabled_until = -1

                elif self.app_config.set_disable_duration == "Until I turn it back on":
                    self.app_config.is_disabled = True
                    self.app_config.disabled_until = -1

                else:
                    self.app_config.is_disabled = True
                    self.app_config.disabled_until = time.time() + disable_time_mapping[self.app_config.set_disable_duration]


                    if time.time() < self.app_config.disabled_until:
                        self.app_config.is_disabled = True
                    else:
                        self.app_config.is_disabled = False
                        self.app_config.disable_duration = "None"
                        self.app_config.disabled_until = -1


                # Only perform the battery check if not disabled.
                if not self.app_config.is_disabled:
                    print("Checking battery status...")
                    status = get_system_power_status()
                    battery_percent = status.BatteryLifePercent
                    if battery_percent != 255 and battery_percent < self.app_config.battery_threshold:
                        self.tray_icon.icon.notify(
                            f"Low Battery: {battery_percent}% remaining",
                            "Low Battery Alert"
                        )
                    if battery_percent == 255:
                        raise Exception("Failed to get battery percentage (got 255, unknown).")
                else:
                    print("Battery monitor is disabled.")

                # time.sleep(self.app_config.battery_query_interval)
                time.sleep(1)
            except Exception as e:
                print("Error checking battery status:", e)
                time.sleep(self.app_config.battery_query_interval)
                raise Exception("Failed to get battery percentage.")

    def load_config(self):
        """
        Loads configuration from a JSON file and initializes the AppConfig.
        Only 'battery_threshold' and 'battery_query_interval' are persisted.
        """
        try:
            with open(self.config_file, "r") as f:
                data = json.load(f)
                self.app_config = AppConfig(
                    battery_threshold=data.get("battery_threshold", 20),
                    battery_query_interval=data.get("battery_query_interval", 60)
                )
        except FileNotFoundError:
            print(f"No config file found ({self.config_file}), using default settings.")
            self.app_config = AppConfig(battery_threshold=20, battery_query_interval=60)
        except Exception as e:
            print("Error loading config:", e)
            self.app_config = AppConfig(battery_threshold=20, battery_query_interval=60)

    def save_config(self):
        """
        Saves the current persistent settings to a JSON configuration file.
        Only battery_threshold and battery_query_interval are saved.
        """
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.app_config.to_dict(), f, indent=4)
            print("Configuration saved to", self.config_file)
        except Exception as e:
            print("Error saving config:", e)

    def run(self):
        """
        Starts the battery monitor thread and launches the tray icon.
        On exit, saves the persistent configuration.
        """
        self.monitor_thread.start()
        try:
            self.tray_icon.run()
        finally:
            self.save_config()


if __name__ == "__main__":
    app = Application("../config/config.json")
    app.run()
