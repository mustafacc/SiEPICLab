"""
SiEPIClab measurement routine.

Testbench for the Keithley class source measure unit class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements


class testbench_smu_keithley(measurements.sequence):
    """Testbench measurement routine for the Keithley class source measure unit class."""

    def __init__(self, smu):
        self.smu = smu
        instruments = [smu]
        self.experiment = measurements.lab_setup(instruments)
        self.verbose = False

    def instructions(self):
        """Sequence of the routine."""
        self.smu.reset()
        if self.verbose:
            print("Testbench ran successfully.")
