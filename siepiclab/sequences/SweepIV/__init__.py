"""
SiEPIClab measurement sequence.

Current-Voltage (IV) sweep using a source measurement unit.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements
import numpy as np


class SweepIV(measurements.sequence):
    """
    Current-Voltage (IV) sweep using a source measurement unit.

    Test setup:
        SMU <-GS-> ||DUT||

    verbose : Boolean, Optional.
        Verbose messages and plots flag. Default is False.
    visual : Boolean, Optional.
        Visualization flag. Default is False.
    """

    def __init__(self, smu):
        self.smu = smu
        self.v_pts = [0]
        self.chan = 'A'
        self.pwr_lim = 10e-3

        self.instruments = [smu]
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

        volt_arr = []
        curr_arr = []
        res_arr = []
        for v in self.v_pts:
            self.smu.SetVoltage(v, self.chan)

            volt_arr.append(self.smu.GetVoltage(self.chan))
            curr_arr.append(self.smu.GetCurrent(self.chan))
            res_arr.append(self.smu.GetResistance(self.chan))

        volt_arr = np.array(volt_arr)
        curr_arr = np.array(curr_arr)
        res_arr = np.array(res_arr)
        if self.visual:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(11, 6))
            plt.plot(volt_arr, 1e3*curr_arr, '.')
            plt.xlabel('Voltage [V]')
            plt.ylabel('Current [mA]')
            plt.title('Result of IVSweep sequence.')
            plt.tight_layout()

            plt.figure(figsize=(11, 6))
            plt.plot(volt_arr, res_arr, '.')
            plt.xlabel('Voltage [V]')
            plt.ylabel('Resistance [Ohms]')
            plt.title('Result of IVSweep sequence.')
            plt.tight_layout()

            plt.figure(figsize=(11, 6))
            plt.plot(volt_arr, volt_arr*curr_arr*1e3, '.')
            plt.xlabel('Voltage [V]')
            plt.ylabel('Power [mW]')
            plt.title('Result of IVSweep sequence.')
            plt.tight_layout()
        if self.verbose:
            print("\n***Sequence executed successfully.***")
