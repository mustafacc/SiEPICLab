"""
SiEPIClab measurement routine.

Testbench for the 11896A polarization controller class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements


class testbench_PolCtrl_keysight(measurements.sequence):
    """
    Testbench measurement routine for the 11896A polarization controller class.

    Testbench for the 11896A polarization controller class.
    """

    def __init__(self, polCtrl):
        self.polCtrl = polCtrl
        instruments = [polCtrl]
        self.experiment = measurements.lab_setup(instruments)

    def instructions(self):
        """Instructions of the sequence."""
        print("Starting scan . . .")
        self.polCtrl.StartScan()
        self.polCtrl.StopScan()

        print("Testbench ran successfully.")
