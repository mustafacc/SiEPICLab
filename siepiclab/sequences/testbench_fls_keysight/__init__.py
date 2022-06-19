"""
SiEPIClab measurement routine.

Testbench for the fixed laser source class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements


class testbench_fls_keysight(measurements.sequence):
    """Testbench measurement routine for the Power Monitor class."""

    def __init__(self, fls):
        self.fls = fls

        instruments = [fls]
        self.experiment = measurements.lab_setup(instruments)

    def instructions(self):
        """Sequence of the routine."""
        print("Testbench ran successfully.")
