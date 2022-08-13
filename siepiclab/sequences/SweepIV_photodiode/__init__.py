"""
SiEPIClab measurement sequence.

Current-Voltage (IV) sweep using a source measurement unit while varying optical input power on a photodiode

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements
import numpy as np
from datetime import datetime
import time


class SweepIV_photodiode(measurements.sequence):
    """
    Current-Voltage (IV) sweep using a source measurement unit and input optical power using a laser on a photodiode.

    Test setup:
        SMU <-GS-> ||DUT||
        laser -SMF-> 3 dB splitter -SMF-> ||DUT||
        laser -SMF-> 3 dB splitter -SMF-> power monitor (reference calibration)

    verbose : Boolean, Optional.
        Verbose messages and plots flag. Default is False.
    visual : Boolean, Optional.
        Visualization flag. Default is False.
    """

    def __init__(self, smu, laser, pm):
        super(SweepIV_photodiode, self).__init__()
        self.smu = smu
        self.v_pts = [0]
        self.chan = 'A'

        self.laser = laser
        self.laser_pwr = [0, 1, 2]  # mW
        self.laser_wavl = 1310  # nm

        self.pm = pm
        self.loss_coupling = 4  # dB

        self.instruments = [smu, laser, pm]
        self.experiment = measurements.lab_setup(self.instruments)

    def instructions(self):
        """Instructions of the sequence."""
        if self.verbose:
            print('\nIdentifying instruments . . .')
            for instr in self.instruments:
                print(instr.identify())
            print('\nDone identifying instruments.')
        self.smu.SetOutput(1, self.chan)

        self.pm.SetWavl(self.laser_wavl)
        self.pm.SetPwrUnit('mW')

        self.laser.SetPwrUnit('mW')
        self.laser.SetWavl(self.laser_wavl)
        self.laser.SetOutput(1)

        volt = np.zeros((np.size(self.v_pts), np.size(self.laser_pwr)))
        curr = np.zeros((np.size(self.v_pts), np.size(self.laser_pwr)))
        res = np.zeros((np.size(self.v_pts), np.size(self.laser_pwr)))
        pm_pwr = []
        laser_pwr = []
        for ii, pwr in enumerate(self.laser_pwr):
            if pwr == 0:
                self.laser.SetOutput(0)
                laser_pwr.append(0)
                pm_pwr.append(0)
            else:
                laser_pwr.append(self.laser.SetPwr(pwr, verbose=True))
                self.laser.SetOutput(1)
                pm_pwr.append(self.pm.GetPwr())
            time.sleep(2)
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
            for idx, p in enumerate(pm_pwr):
                plt.semilogy(volt[:, idx], 1e9*np.abs(curr[:, idx]),
                             '.', label=f"Input {10*np.log10(p)-self.loss_coupling} dBm")
            plt.legend()
            plt.xlabel('Voltage [V]')
            plt.ylabel('Current [nA]')
            plt.title('Result of SweepIV_photodiode sequence.')
            plt.tight_layout()
            if self.saveplot:
                fname = str(datetime.now().strftime('%Y%m%d%H%M%S'))
                plt.savefig(fname+'_SweepIV_photodiode.pdf')

        if self.verbose:
            print("\n***Sequence executed successfully.***")

        return volt, curr, res, laser_pwr
