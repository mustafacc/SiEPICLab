"""
SiEPIClab measurement sequence.

Polarization optimization sequence.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements


class OptimizePolarization(measurements.sequence):
    """
    Polarization optimization sequence.

    Test setup:
        laser -SMF-> polarization controller -SMF-> ||DUT|| -SMF-> Power Monitor

    scantime : int, Optional.
        Scan time of the polarization controller (seconds). Default is 15 secs.
    wavl : int, Optional.
        Wavelength to perform the sequence at (nm). Default is 1550 nm.
    scanrate : int, Optional.
        Scan rate of the polarization controller (1 = slowest, 8 = fastest).
        Default is 1.
    verbose : Boolean, Optional.
        Verbose messages and plots flag. Default is False.
    """

    def __init__(self, fls, polCtrl, pm, scantime=15, wavl=1550, scanrate=1, verbose=False):
        self.fls = fls
        self.polCtrl = polCtrl
        self.pm = pm
        self.scantime = scantime
        self.wavl = wavl
        self.scanrate = scanrate
        self.verbose = verbose
        self.instruments = [fls, polCtrl, pm]
        self.experiment = measurements.lab_setup(self.instruments)

    def instructions(self):
        """Instructions of the sequence."""
        import time

        if self.verbose:
            print('Identifying instruments . . .')
            for instr in self.instruments:
                print(instr.identify())
            print('Done identifying instruments.')

        # set the laser to the desired wavelength.
        self.fls.SetWavl(self.wavl)
        self.polCtrl.SetScanRate(self.scanrate)
        # set the detector to the wavelength
        # turn on the laser

        samples = []
        pm_data = []
        if self.verbose:
            print("Starting scan . . .")
        self.polCtrl.StartScan()
        timeStop = time.monotonic() + self.scantime

        while time.monotonic() < timeStop:
            samples.append(self.polCtrl.GetPaddlePositionAll())
            pm_data.append(self.pm.GetPwr())
        self.polCtrl.StopScan()

        if self.verbose:
            print("Sequence ran successfully.")
