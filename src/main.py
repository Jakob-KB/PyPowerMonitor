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
import logging

from config import DEFAULT_QUERY_INTERVAL, ALERT_QUERY_INTERVAL, DEFAULT_BATTERY_THRESHOLD


@dataclass
class AppConfig:
    battery_threshold: int
    query_interval: int
    enabled: bool = True


class PyPowerMonitor:
    app_config: AppConfig

    def __init__(self):
        self.app_config = AppConfig(
            battery_threshold=DEFAULT_BATTERY_THRESHOLD,
            query_interval=DEFAULT_QUERY_INTERVAL
        )

        self.tray_icon = Tray(self.app_config)
        self.monitor_thread = threading.Thread(
            target=self.power_monitor, daemon=True
        )

    def power_monitor(self):
        """
        Monitor the power status of the system and manage the application
        """
        while True:
            try:
                # Check if power monitoring is enabled
                if self.app_config.enabled:
                    # Retrieve current power status from the system
                    status = get_system_power_status()
                    battery_percent = status.BatteryLifePercent
                    battery_charging = bool(status.ACLineStatus)

                    # Validate battery percentage
                    if battery_percent == 255 or battery_percent < 0 or battery_percent > 100:
                        raise ValueError(f"Unexpected battery percentage status: {battery_percent}%.")

                    # Determine query interval and whether to launch a notification
                    if battery_charging or battery_percent > self.app_config.battery_threshold:
                        self.app_config.query_interval = DEFAULT_QUERY_INTERVAL
                    else:
                        self.app_config.query_interval = ALERT_QUERY_INTERVAL
                        self.tray_icon.icon.notify(
                            f"Low Battery: {battery_percent}% remaining",
                            "Low Battery Alert"
                        )
                else:
                    self.app_config.query_interval = DEFAULT_QUERY_INTERVAL
                    logging.info("Power monitoring is disabled.")
            except ValueError as e:
                logging.warning("Unexpected Value Error: %s", e)
            except Exception as e:
                logging.warning("Unexpected Exception: %s", e)
            finally:
                # Pause until the next battery status query
                time.sleep(self.app_config.query_interval)

    def run(self):
        """
        Starts the battery monitor thread and launches the tray icon.
        """
        self.monitor_thread.start()
        self.tray_icon.run()


if __name__ == "__main__":
    app = PyPowerMonitor()
    app.run()
