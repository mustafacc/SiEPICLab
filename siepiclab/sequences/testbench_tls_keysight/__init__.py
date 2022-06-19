"""
SiEPIClab measurement routine.

Testbench for the tunable laser source class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements


class testbench_tls_keysight(measurements.sequence):
    """Testbench measurement sequence for the tunable laser source class."""

    def __init__(self, tls):
        self.tls = tls

        instruments = [tls]
        self.experiment = measurements.lab_setup(instruments)

    def instructions(self):
        """Sequence of the routine."""
        print("Testbench ran successfully.")
