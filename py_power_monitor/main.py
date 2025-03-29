#!/usr/bin/env python3
"""
Module: main.py

Entry point for the application.
"""

import threading
from battery import get_system_power_status
from tray import Tray


from dataclasses import dataclass
import time

@dataclass
class AppConfig:
    battery_threshold: int
    battery_query_interval: int
    is_disabled: bool = False


class PyPowerMonitor:
    app_config: AppConfig

    def __init__(self):
        self.app_config = AppConfig(
            battery_threshold=10,
            battery_query_interval=30
        )

        # Create the tray icon using the Tray class, passing the app config
        self.tray_icon = Tray(self.app_config)
        self.monitor_thread = threading.Thread(
            target=self.battery_monitor, daemon=True
        )

    def battery_monitor(self):
        """
        Continuously monitors the battery status.
        """
        while True:
            try:
                # Only perform the battery check if not disabled
                if not self.app_config.is_disabled:
                    status = get_system_power_status()
                    battery_percent = status.BatteryLifePercent
                    if battery_percent != 255 and battery_percent < self.app_config.battery_threshold:
                        self.tray_icon.icon.notify(
                            f"Low Battery: {battery_percent}% remaining",
                            "Low Battery Alert"
                        )
                        print(f"Low battery: {battery_percent}% remaining")
                    if battery_percent == 255:
                        print("Error: Received unknown battery percentage (255).")
                else:
                    print("Battery monitor is disabled.")

                time.sleep(self.app_config.battery_query_interval)
            except Exception as e:
                print("Error checking battery status:", e)
                time.sleep(self.app_config.battery_query_interval)
                # Do not re-raise the exception; continue monitoring.

    def run(self):
        """
        Starts the battery monitor thread and launches the tray icon.
        On exit, saves the persistent configuration.
        """
        self.monitor_thread.start()
        self.tray_icon.run()


if __name__ == "__main__":
    app = PyPowerMonitor()
    app.run()
