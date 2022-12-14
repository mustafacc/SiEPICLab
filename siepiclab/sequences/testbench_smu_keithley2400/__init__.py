"""
SiEPIClab measurement routine.

Testbench for the Keithley 2400 class source measure unit class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements


class testbench_smu_keithley2400(measurements.sequence):
    """Testbench measurement routine for the Keithley 2400 class source measure unit class."""

    def __init__(self, smu):
        super().__init__(self)
        self.smu = smu
        self.instruments.append(smu)
        self.experiment = measurements.lab_setup(self.instruments)

    def instructions(self):
        """Sequence of the routine."""
        self.smu.reset()
        if self.verbose:
            print("Testbench ran successfully.")
