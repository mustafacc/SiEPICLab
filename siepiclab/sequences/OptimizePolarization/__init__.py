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
    pwr : float, Optional.
        Power to use for the laser output (mW). Default is 1 mW.
    wavl : int, Optional.
        Wavelength to perform the sequence at (nm). Default is 1550 nm.
    scanrate : int, Optional.
        Scan rate of the polarization controller (1 = slowest, 8 = fastest).
        Default is 1.
    verbose : Boolean, Optional.
        Verbose messages and plots flag. Default is False.
    visual : Boolean, Optional.
        Visualization flag. Default is False.
    """

    def __init__(self, fls, polCtrl, pm, scantime=15, pwr=1, wavl=1550,
                 scanrate=1, verbose=False, visual=False):
        self.fls = fls
        self.polCtrl = polCtrl
        self.pm = pm
        self.scantime = scantime
        self.pwr = pwr
        self.wavl = wavl
        self.scanrate = scanrate
        self.verbose = verbose
        self.visual = visual
        self.instruments = [fls, polCtrl, pm]
        self.experiment = measurements.lab_setup(self.instruments)

    def InstrSetting(self):
        """Instruments setting."""
        # set the polarization controller scan rate
        self.polCtrl.SetScanRate(self.scanrate)
        # set the detector to the wavelength and units to mW
        self.pm.SetWavl(self.wavl)
        self.pm.SetPwrUnit('mW')
        # set the wavelength and power of the laser and turn on
        self.fls.SetWavl(self.wavl)
        self.fls.SetPwrUnit('dBm')
        self.fls.SetPwr(self.pwr)
        self.fls.SetPwrUnit('mW')
        self.fls.SetOutput(True)

    def instructions(self):
        """Instructions of the sequence."""
        import time
        import numpy as np

        if self.verbose:
            print('\nIdentifying instruments . . .')
            for instr in self.instruments:
                print(instr.identify())
            print('\nDone identifying instruments.')

        self.InstrSetting()

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
        pm_data = 10*np.log10(np.array(pm_data))

        if self.visual:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(11, 6))
            plt.plot(pm_data, '.')
            plt.xlabel('Sample')
            plt.ylabel('Power [dBm]')
            title1 = 'Polarization optimization sweep sequence\n'
            title2 = f'scanrate = {self.scanrate}, pwr = {10*np.log10(self.pwr)} dBm\n'
            title3 = f'wavl = {int(self.wavl)} nm, scantime = {self.scantime}'

            plt.title(title1+title2+title3)
            plt.tight_layout()
        if self.verbose:
            print("\n***Sequence executed successfully.***")
