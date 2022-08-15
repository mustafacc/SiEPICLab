"""
SiEPIClab measurement sequence.

Polarization sweep sequence.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements


class SetupLDC501(measurements.sequence):
    """
    Polarization sweep sequence.

    Test setup:
        laser -SMF-> polarization controller -SMF-> ||DUT|| -SMF-> Power Monitor

    scantime : int, Optional.
        Scan time of the polarization controller (seconds). Default is 15 secs.
    pwr : float, Optional.
        Power to use for the laser output (mW). Default is 1 mW.
    wavl : int, Optional.
        Wavelength to perform the sequence at (nm). Default is 1550 nm.
    scanrate : int, Optional.
        Scan rate of the polarization controller (1 = slowest, 8 = fastest).
        Default is 1.
    optimize : Boolean, Optional.
        Optimization flag. Sets the polarization controller to maximize transmission.
        Default is True.
    verbose : Boolean, Optional.
        Verbose messages and plots flag. Default is False.
    visual : Boolean, Optional.
        Visualization flag. Default is False.
    """

    def __init__(self, ldc):
        self.ldc = ldc

        self.optimize = False
        self.verbose = False
        self.visual = False

        self.instruments = [ldc]
        self.experiment = measurements.lab_setup(self.instruments)

    def InstrSetting(self):
        pass

    def instructions(self):
        pass
        