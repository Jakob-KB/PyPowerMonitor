#!/usr/bin/env python3
"""
Module: main.py

Entry point for the application, controlling and starting the power monitor thread.
"""

import threading
import time
from battery import get_system_power_status
from tray import create_tray_icon
from config import BATTERY_THRESHOLD, BATTERY_CHECK_INTERVAL

ENABLED = True


def battery_monitor(tray_icon):
    """
    Monitors battery life and notifies if below threshold.
    """
    while ENABLED:
        try:
            status = get_system_power_status()
            battery_percent = status.BatteryLifePercent
            if battery_percent != 255 and battery_percent < BATTERY_THRESHOLD:
                tray_icon.notify(
                    f"Low Battery: {battery_percent}% remaining",
                    "Low Battery Alert"
                )
            if battery_percent == 255:
                raise Exception("Failed to get battery percentage, got 255 error unknown.")
            time.sleep(BATTERY_CHECK_INTERVAL)
        except Exception as e:
            print("Error checking battery status:", e)
            time.sleep(BATTERY_CHECK_INTERVAL)

if __name__ == "__main__":
    tray_icon = create_tray_icon()
    monitor_thread = threading.Thread(target=battery_monitor, args=(tray_icon,), daemon=True)
    monitor_thread.start()
    tray_icon.run()
