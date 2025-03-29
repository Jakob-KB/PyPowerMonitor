#! /usr/bin/env python3
"""
Module: battery.py

Uses ctypes to retrieve system power status from the Windows API.
"""

import ctypes
from ctypes import c_byte, c_ulong, Structure


class SYSTEM_POWER_STATUS(Structure):
    """
    Current power status of the system, retrieved from the Windows API.
    """
    _fields_ = [
        ("ACLineStatus", c_byte),  # Power connection status flags
        ("BatteryFlag", c_byte),  # Battery status flags
        ("BatteryLifePercent", c_byte),  # Battery percentage
        ("SystemStatusFlag", c_byte),  # Reserved
        ("BatteryLifeTime", c_ulong),  # Seconds of battery life remaining
        ("BatteryFullLifeTime", c_ulong)  # Seconds of full battery life
    ]


def get_system_power_status() -> SYSTEM_POWER_STATUS:
    """
    Retrieves the current power status of the system using the Windows API.

    :rtype: SYSTEM_POWER_STATUS
    :returns:
        An instance of SYSTEM_POWER_STATUS containing the current system power information.
    :raises Exception:
        If the retrieval of the system power status fails.
    """
    # Call the GetSystemPowerStatus function from kernel32.dll
    status = SYSTEM_POWER_STATUS()
    result = ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status))

    # Check if the result is valid, if not raise an exception
    if result:
        return status
    else:
        raise Exception("Failed to get system power status")
        # Could instead: raise ctypes.WinError()
