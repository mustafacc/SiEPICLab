"""
SiEPIClab measurement sequence.

Current-Voltage (IV) sweep using a source measurement unit while varying optical input power

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements
import numpy as np
from datetime import datetime


class SweepIV_opticalinput(measurements.sequence):
    """
    Current-Voltage (IV) sweep using a source measurement unit and input optical power using a laser.

    Test setup:
        SMU <-GS-> ||DUT||
        laser -SMF-> ||DUT||

    verbose : Boolean, Optional.
        Verbose messages and plots flag. Default is False.
    visual : Boolean, Optional.
        Visualization flag. Default is False.
    """

    def __init__(self, smu, laser):
        super(SweepIV_opticalinput, self).__init__()
        self.smu = smu
        self.v_pts = [0]
        self.chan = 'A'
        self.pwr_lim = 10e-3

        self.laser = laser
        self.laser_pwr = [0, 1, 2]  # mW
        self.laser_wavl = 1310  # nm
        self.instruments = [smu, laser]
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

        self.laser.SetPwrUnit('mW')
        self.laser.SetWavl(self.laser_wavl)
        self.laser.SetOutput(1)

        volt = np.zeros((np.size(self.v_pts), np.size(self.laser_pwr)))
        curr = np.zeros((np.size(self.v_pts), np.size(self.laser_pwr)))
        res = np.zeros((np.size(self.v_pts), np.size(self.laser_pwr)))
        laser_pwr = []
        for ii, pwr in enumerate(self.laser_pwr):
            if pwr == 0:
                self.laser.SetOutput(0)
                laser_pwr.append(0)
            else:
                laser_pwr.append(self.laser.SetPwr(pwr, verbose=True))
                self.laser.SetOutput(1)
            for idx, v in enumerate(self.v_pts):
                self.smu.SetVoltage(v, self.chan)
                volt[idx, ii] = self.smu.GetVoltage(self.chan)
                curr[idx, ii] = self.smu.GetCurrent(self.chan)
                res[idx, ii] = self.smu.GetResistance(self.chan)

            volt = np.array(volt)
            curr = np.array(curr)
            res = np.array(res)

            self.results.add('volt', volt)
            self.results.add('curr', curr)
            self.results.add('res', res)
            self.results.add('laser_pwr', laser_pwr)

        if self.visual:
            import matplotlib.pyplot as plt

            plt.figure(figsize=(11, 6))
            for idx, p in enumerate(laser_pwr):
                plt.plot(volt[:, idx], 1e3*curr[:, idx], '.', label='Input = '+str(p) + ' mW')
            plt.legend()
            plt.xlabel('Voltage [V]')
            plt.ylabel('Current [mA]')
            plt.title('Result of SweepIV_opticalinput sequence.')
            plt.tight_layout()
            if self.saveplot:
                fname = str(datetime.now().strftime('%Y%m%d%H%M%S'))
                plt.savefig(fname+'_SweepIV_opticalinput.pdf')

        if self.verbose:
            print("\n***Sequence executed successfully.***")

        return volt, curr, res, laser_pwr
