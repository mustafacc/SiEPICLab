"""
SiEPIClab measurement routine.

Testbench for the fixed laser source class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements


class testbench_fls_keysight(measurements.sequence):
    """Testbench measurement sequence for the fixed laser source class."""

    def __init__(self, fls):
        super().__init__(self)
        self.fls = fls

        self.verbose = False
        
        self.instruments.append(fls)
        self.experiment = measurements.lab_setup(self.instruments)

    def instructions(self):
        """Sequence of the routine."""
        print("Testbench ran successfully.")
