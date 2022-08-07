"""
SiEPIClab measurement sequence.

Photodiode respinsivity measurement sequence.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements
import numpy as np
from datetime import datetime


class PD_Responsivity(measurements.sequence):
    """
    Current-Voltage (IV) sweep using a source measurement unit.

    Test setup:
        SMU <-electrical_GS-> ||DUT||
        laser -optical-> 3 dB splitter -optical-> ||DUT||
        laser -optical-> 3 dB splitter -optical-> reference calibration monitor

    verbose : Boolean, Optional.
        Verbose messages and plots flag. Default is False.
    visual : Boolean, Optional.
        Visualization flag. Default is False.
    """

    def __init__(self, smu, pm, laser):
        super(PD_Responsivity, self).__init__()
        self.smu = smu
        self.smu_v_bias = 0
        self.chan = 'A'

        self.pm = pm

        self.laser = laser
        self.wavl_start = 1480  # nm
        self.wavl_stop = 1580  # nm
        self.wavl_pts = 501
        self.laser_pwr = 1  # mW

        self.instruments = [smu, pm, laser]
        self.experiment = measurements.lab_setup(self.instruments)

    def instructions(self):
        """Instructions of the sequence."""
        if self.verbose:
            print('\nIdentifying instruments . . .')
            for instr in self.instruments:
                print(instr.identify())
            print('\nDone identifying instruments.')

        wavl_range = np.linspace(self.wavl_start, self.wavl_stop, self.wavl_pts)
        self.smu.SetVoltage(self.smu_v_bias, self.chan)
        self.smu.SetOutput(1, self.chan)

        self.pm.SetPwrUnit('mW')

        self.laser.SetPwrUnit('mW')
        self.laser.SetOutput(1)

        photocurr = []
        wavls = []
        pwr_optical = []
        for wavl in wavl_range:
            wavls.append(self.laser.SetWavl(wavl, verbose=True))
            photocurr.append(self.smu.GetCurrent(self.chan))
            pwr_optical.append(self.pm.GetPwr())

        photocurr = np.abs(np.array(photocurr))
        pwr_optical = np.array(pwr_optical)

        responsivity = photocurr/(1e-3*pwr_optical)  # A/W

        self.results.add('photocurr', photocurr)
        self.results.add('wavls', wavls)
        self.results.add('pwr_optical', pwr_optical)
        self.results.add('responsivity', responsivity)

        if self.visual:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(11, 6))
            plt.plot(wavls, responsivity, '.')
            plt.legend()
            plt.xlabel('Wavelength [nm]')
            plt.ylabel('Responsivity [A/W]')
            plt.title('Result of PD_responsivity sequence.')
            plt.tight_layout()
            if self.saveplot:
                fname = str(datetime.now().strftime('%Y%m%d%H%M%S'))
                plt.savefig(fname+'_PD_responsivity.pdf')

            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            ax1.plot(wavls, pwr_optical, '.', color='green')
            ax2.plot(wavls, photocurr*1e6, '.', color='blue')
            ax1.set_xlabel('Wavelength [nm]')
            ax1.set_ylabel('Optical reference power (mW)', color='g')
            ax2.set_ylabel('|PD Photocurrent (µA)|', color='b')
            plt.title('Result of PD_responsivity sequence.')
            plt.tight_layout()
            if self.saveplot:
                fname = str(datetime.now().strftime('%Y%m%d%H%M%S'))
                plt.savefig(fname+'_PD_responsivity_photocurr_optical.pdf')

        if self.verbose:
            print("\n***Sequence executed successfully.***")

        return photocurr, wavls, pwr_optical, responsivity
