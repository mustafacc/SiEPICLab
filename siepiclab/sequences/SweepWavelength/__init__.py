"""
SiEPIClab measurement sequence.

Wavelength sweep sequence using tunable laser source and optical power monitor.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements


class SweepWavelength(measurements.sequence):
    """
    Wavelength sweep sequence using tunable laser source and optical power monitor.

    Test setup:
        laser -SMF-> ||DUT|| -SMF-> Power Monitor(s)

    verbose : Boolean, Optional.
        Verbose messages and plots flag. Default is False.
    visual : Boolean, Optional.
        Visualization flag. Default is False.
    """

    def __init__(self, tls, pm):
        self.tls = tls
        self.pm = pm

        # sequnece default settings
        self.wavlStart = 1280  # nm
        self.wavlStop = 1380  # nm
        self.wavlPts = 1001  # number of points
        self.pwr = 1  # laser power, mW
        self.sweepSpeed = 20  # nm/s
        self.upperLimit = -100  # maximum power expected (dbm, -100: existing setting.)
        self.verbose = False
        self.visual = False

        self.instruments = [tls, pm]
        self.experiment = measurements.lab_setup(self.instruments)

        self.wavl = int((self.wavlStop-self.wavlStart)/2)
        self.res = 1e3*(self.wavlStop-self.wavlStart)/(self.wavlPts-1)

    def InstrSetting(self):
        """Instruments setting."""
        # set the detector to the wavelength and units to mW
        self.pm.SetWavl(self.wavl)
        self.pm.SetPwrUnit('mW')
        # set the wavelength and power of the laser and turn on
        self.tls.SetWavl(self.wavl)
        self.tls.SetPwrUnit('dBm')
        self.tls.SetPwr(self.pwr)
        self.tls.SetPwrUnit('mW')
        self.tls.SetOutput(True)

    def instructions(self):
        """Instructions of the sequence."""
        if self.verbose:
            print('\nIdentifying instruments . . .')
            for instr in self.instruments:
                print(instr.identify())
            print('\nDone identifying instruments.')

        self.InstrSetting()

        if self.verbose:
            print("\n***Sequence executed successfully.***")
