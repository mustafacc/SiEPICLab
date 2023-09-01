"""
SiEPIClab measurement sequence.

OSA Scan sequence.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements

from drivers.osa_agilent import osa_agilent

class OSA_scan(measurements.sequence):

    def __init__(self, osa, visual=False, verbose=False, saveplot=False):
        super().__init__(visual, verbose, saveplot)
        self.osa = osa

    def InstrSetting(self):
        self.osa.
        pass

    def instructions(self):
        if self.verbose:
            print('\nIdentifying instruments . . .')
        for instr in self.instruments:
            print(instr.identify())
        print('\nDone identifying instruments.')

        self.InstrSetting()

        self.osa.scan()