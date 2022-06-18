"""
SiEPIClab measurement routine.

Testbench for the 81635A Power Monitor class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements


class testbench_PowerMonitor_keysight(measurements.sequence):
    """Testbench measurement routine for the Power Monitor class."""

    def __init__(self, pm):
        self.pm = pm
        instruments = [pm]
        self.experiment = measurements.lab_setup(instruments)

    def instructions(self):
        """Sequence of the routine."""
        print(self.pm.identify())
        print('Power reading: ' + str(self.pm.GetPwr()))

        print("Testbench ran successfully.")
