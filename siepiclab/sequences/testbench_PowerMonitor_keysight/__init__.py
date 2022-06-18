"""
SiEPIClab measurement routine.

Testbench for the 81635A Power Monitor class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements


class testbench_PowerMonitor_keysight(measurements.sequence):
    """Testbench measurement routine for the Power Monitor class."""

    def __init__(self, pm, pwrUnit, wavl):
        self.pm = pm
        self.pwrUnit = pwrUnit
        self.wavl = wavl

        instruments = [pm]
        self.experiment = measurements.lab_setup(instruments)

    def instructions(self):
        """Sequence of the routine."""
        import time

        print('Power unit reading: ' + str(self.pm.GetPwrUnit()))
        print('Wavelength reading: ' + str(self.pm.GetWavl()))

        print('Setting power unit to: '+str(self.pwrUnit))
        result = self.pm.SetPwrUnit(self.pwrUnit, confirm=True)
        print('Reading power unit at: '+str(result))

        print('Setting wavelength to: '+str(self.wavl))
        result = self.pm.SetWavl(self.wavl, confirm=True)
        print('Reading wavelength at: '+str(result))

        time.sleep(5)
        print("Testbench ran successfully.")
