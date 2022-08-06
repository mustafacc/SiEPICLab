"""
SiEPIClab measurement sequence.

Current-Voltage (IV) sweep using a source measurement unit while recording optical power.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements
import numpy as np


class SweepIV_optical(measurements.sequence):
    """
    Current-Voltage (IV) sweep using a source measurement unit.

    Test setup:
        SMU <-GS-> ||DUT||

    verbose : Boolean, Optional.
        Verbose messages and plots flag. Default is False.
    visual : Boolean, Optional.
        Visualization flag. Default is False.
    """

    def __init__(self, smu, pm):
        super(SweepIV_optical, self).__init__()
        self.smu = smu
        self.v_pts = [0]
        self.chan = 'A'
        self.pwr_lim = 10e-3

        self.pm = pm
        # if user configures only a single power monitor not then make it a list
        if type(self.pm) != list:
            self.pm = [self.pm]

        self.instruments = [smu]+self.pm
        self.experiment = measurements.lab_setup(self.instruments)

    def instructions(self):
        """Instructions of the sequence."""
        if self.verbose:
            print('\nIdentifying instruments . . .')
            for instr in self.instruments:
                print(instr.identify())
            print('\nDone identifying instruments.')
        self.smu.SetPowerLimit(self.pwr_lim, self.chan)
        self.smu.SetOutput(1, self.chan)
        for p in self.pm:
            p.SetPwrUnit('mW')

        volt = []
        curr = []
        res = []
        pwr_optical = np.zeros((np.size(self.v_pts), len(self.pm)))
        for idx, v in enumerate(self.v_pts):
            self.smu.SetVoltage(v, self.chan)

            volt.append(self.smu.GetVoltage(self.chan))
            curr.append(self.smu.GetCurrent(self.chan))
            res.append(self.smu.GetResistance(self.chan))
            for pm_idx, p in enumerate(self.pm):
                pwr_optical[idx, pm_idx] = p.GetPwr()

        volt = np.array(volt)
        curr = np.array(curr)
        res = np.array(res)
        pwr_optical = np.array(pwr_optical)

        self.results.add('volt', volt)
        self.results.add('curr', curr)
        self.results.add('res', res)
        self.results.add('pwr_optical', pwr_optical)

        if self.visual:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(11, 6))
            plt.plot(volt, 1e3*curr, '.')
            plt.xlabel('Voltage [V]')
            plt.ylabel('Current [mA]')
            plt.title('Result of IVSweep sequence.')
            plt.tight_layout()

            plt.figure(figsize=(11, 6))
            plt.plot(volt, res, '.')
            plt.xlabel('Voltage [V]')
            plt.ylabel('Resistance [Ohms]')
            plt.title('Result of IVSweep sequence.')
            plt.tight_layout()

            plt.figure(figsize=(11, 6))
            plt.plot(volt, volt*curr*1e3, '.')
            plt.xlabel('Voltage [V]')
            plt.ylabel('Power [mW]')
            plt.title('Result of IVSweep sequence.')
            plt.tight_layout()

            plt.figure(figsize=(11, 6))
            for idx, p in enumerate(self.pm):
                plt.plot(volt, 10*np.log10(pwr_optical[:, idx]), '.')
            plt.legend(['CH'+str(ii) for ii, jj in enumerate(self.pm)])
            plt.xlabel('Voltage [V]')
            plt.ylabel('Optical Power [dB]')
            plt.title('Result of IVSweep sequence.')
            plt.tight_layout()

            plt.figure(figsize=(11, 6))
            for idx, p in enumerate(self.pm):
                plt.plot(volt*curr*1e3, 10*np.log10(pwr_optical[:, idx]), '.')
            plt.legend(['CH'+str(ii) for ii, jj in enumerate(self.pm)])
            plt.xlabel('Electrical Power [mW]')
            plt.ylabel('Optical Power [dB]')
            plt.title('Result of IVSweep sequence.')
            plt.tight_layout()
        if self.verbose:
            print("\n***Sequence executed successfully.***")

        return volt, curr, res, pwr_optical
