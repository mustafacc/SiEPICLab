"""
SiEPIClab measurement routine.

Testbench for the tunable laser source class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements


class testbench_tls_keysight(measurements.sequence):
    """Testbench measurement sequence for the tunable laser source class."""

    def __init__(self, tls):
        super().__init__(self)
        self.tls = tls

        self.instruments.append(tls)
        self.experiment = measurements.lab_setup(self.instruments)

    def instructions(self):
        """Sequence of the routine."""
        print("Testbench ran successfully.")
