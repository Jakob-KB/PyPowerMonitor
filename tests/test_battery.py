#!/usr/bin/env python3
"""
Test: test_battery.py

Run tests on the battery module to check that it can successfully retrieve system power status and handle
a failed retrieval.
"""

import unittest
from unittest.mock import patch
import ctypes
from py_power_monitor.battery import get_system_power_status, SYSTEM_POWER_STATUS


class TestGetSystemPowerStatus(unittest.TestCase):
    def test_successful_call(self):
        # Create a fake SYSTEM_POWER_STATUS with sample values
        fake_status = SYSTEM_POWER_STATUS()

        fake_status.ACLineStatus = 1  # Online
        fake_status.BatteryFlag = 1  # High battery
        fake_status.BatteryLifePercent = 85  # 85%
        fake_status.SystemStatusFlag = 0  # Reserved, typically 0
        fake_status.BatteryLifeTime = 3600  # 1 hour remaining
        fake_status.BatteryFullLifeTime = 7200  # 2 hours full life

        # Side effect function to simulate the Windows API populating the status structure
        def side_effect(status_ptr):
            # Cast the CArgObject to a pointer of SYSTEM_POWER_STATUS
            status = ctypes.cast(status_ptr, ctypes.POINTER(SYSTEM_POWER_STATUS)).contents

            status.ACLineStatus = fake_status.ACLineStatus
            status.BatteryFlag = fake_status.BatteryFlag
            status.BatteryLifePercent = fake_status.BatteryLifePercent
            status.SystemStatusFlag = fake_status.SystemStatusFlag
            status.BatteryLifeTime = fake_status.BatteryLifeTime
            status.BatteryFullLifeTime = fake_status.BatteryFullLifeTime

            return 1  # non-zero indicates success

        # Patch the Windows API call
        with patch("ctypes.windll.kernel32.GetSystemPowerStatus", side_effect=side_effect):
            result = get_system_power_status()

            # Assert that results are what is expected
            self.assertEqual(result.ACLineStatus, fake_status.ACLineStatus)
            self.assertEqual(result.BatteryFlag, fake_status.BatteryFlag)
            self.assertEqual(result.BatteryLifePercent, fake_status.BatteryLifePercent)
            self.assertEqual(result.SystemStatusFlag, fake_status.SystemStatusFlag)
            self.assertEqual(result.BatteryLifeTime, fake_status.BatteryLifeTime)
            self.assertEqual(result.BatteryFullLifeTime, fake_status.BatteryFullLifeTime)

    def test_failure_call(self):
        # Patch the API to return 0, simulating a failure
        with patch("ctypes.windll.kernel32.GetSystemPowerStatus", return_value=0):
            with self.assertRaises(Exception) as context:
                get_system_power_status()
            self.assertIn("Failed to get system power status", str(context.exception))


if __name__ == "__main__":
    unittest.main()
