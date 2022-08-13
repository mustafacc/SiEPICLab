"""
SiEPIClab measurement sequence.

Photodiode respinsivity measurement sequence.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements
import numpy as np
from datetime import datetime
import time


class photodiode_responsivity(measurements.sequence):
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
        super(photodiode_responsivity, self).__init__()
        self.smu = smu
        self.smu_v_bias = [0, -1, -2]

        self.smu_chan = 'A'

        self.pm = pm
        self.loss_coupling = 5  # dB

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

        # if user configures only a single power monitor not then make it a list
        if type(self.smu_v_bias) != list:
            self.smu_v_bias = [self.smu_v_bias]

        wavl_range = np.linspace(self.wavl_start, self.wavl_stop, self.wavl_pts)
        self.smu.SetVoltage(0, self.smu_chan)
        self.smu.SetOutput(1, self.smu_chan)

        self.pm.SetPwrUnit('dBm')

        self.laser.SetPwrUnit('mW')
        self.laser.SetPwr(self.laser_pwr)
        self.laser.SetOutput(1)

        photocurr = np.zeros((np.size(wavl_range), np.size(self.smu_v_bias)))
        wavls = np.zeros((np.size(wavl_range), np.size(self.smu_v_bias)))
        pwr_optical = np.zeros((np.size(wavl_range), np.size(self.smu_v_bias)))
        responsivity = np.zeros((np.size(wavl_range), np.size(self.smu_v_bias)))

        # create a polynomial fit for the responsivity model
        wavl_res = 0.1  # 100 pm
        wavls_fit = np.arange(np.min(wavl_range), np.max(wavl_range), wavl_res)
        responsivity_fit = np.zeros((np.size(wavls_fit), np.size(self.smu_v_bias)))
        for i, volt in enumerate(self.smu_v_bias):
            self.smu.SetVoltage(volt, self.smu_chan)
            time.sleep(2)
            for idx, wavl in enumerate(wavl_range):
                wavls[idx, i] = self.laser.SetWavl(wavl, verbose=True)
                photocurr[idx, i] = self.smu.GetCurrent(self.smu_chan)
                pwr_optical[idx, i] = 10**((1e-3*self.pm.GetPwr()+self.loss_coupling)/10)

            photocurr[:, i] = np.abs(photocurr[:, i])
            responsivity[:, i] = photocurr[:, i] / (1e-3*pwr_optical[:, i])  # A/W
            # 3rd order polynomial usually okay for broadband responsivity plots
            pfit = np.poly1d(np.polyfit(wavls[:, i], responsivity[:, i], 3))
            responsivity_fit[:, i] = pfit(wavls_fit)

        self.results.add('wavls', wavls)
        self.results.add('responsivity', responsivity)
        self.results.add('wavls_fit', wavls_fit)
        self.results.add('responsivity_fit', responsivity_fit)
        self.results.add('pwr_optical', pwr_optical)
        self.results.add('photocurr', photocurr)

        if self.visual:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(11, 6))
            for i, volt in enumerate(self.smu_v_bias):
                plt.plot(wavls[:, i], responsivity[:, i],
                         '.', label=f"Experiment (V = {volt} V)")
                plt.plot(wavls_fit, responsivity_fit[:, i], label=f"Model (V = {volt} V)")
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
            for i, volt in enumerate(self.smu_v_bias):
                ax1.plot(wavls[:, i], pwr_optical[:, i],
                         '.', color='green', label=f"V = {volt} V")
                ax2.plot(wavls[:, i], photocurr[:, i]*1e6,
                         '.', color='blue', label=f"V = {volt} V")
            plt.legend()
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
