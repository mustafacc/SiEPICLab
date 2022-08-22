"""
SiEPIClab measurement sequence.

Polarization optimization and Measurement through Switch Paths

Davin Birdi, UBC Photonics, 2022
"""
from tabnanny import verbose
from siepiclab import measurements
from siepiclab.sequences.SwitchPath import SwitchPath
from siepiclab.sequences.SweepPolarization import SweepPolarization
import numpy as np


class SweepPolarization_SwitchPaths(SweepPolarization):
    """
    Wavelength spectrum sweep sequence using tunable laser source and optical power monitor.

    Test setup:
        Optical:    laser -SMF-> ||DUT|| -SMF-> Power Monitor(s)
        Electrical: smu -GS-> ||DUT||

    verbose : Boolean, Optional.
        Verbose messages and plots flag. Default is False.
    visual : Boolean, Optional.
        Visualization flag. Default is False.
    """

    def __init__(self, fls, pol, pm, jds):
        super().__init__(fls, pol, pm)
        
        SwitchPath.__init__(self, jds)
        
        #self.jds = jds

        self.scantime = 45
        self.optimize = True
        self.range = [1, 2, 3]

        #self.instruments.append(jds)
        self.experiment = measurements.lab_setup(self.instruments)

    def instructions(self):
        """Instructions of the sequence."""
        
        if self.verbose:
            print("\n***Sequence Starting...***")

        rslts_pm = []

        for i in self.range:
            self.chan = i
            if self.verbose:
                print("\n***Switch Changing...***")
            SwitchPath.instructions(self)
            if self.verbose:
                print("\n***Optimizing Polarization...***")
            temp = SweepPolarization.instructions(self)
            rslts_pm.append(max(temp))
            if self.sweep == True:
                pass

            pass

        self.results.add('rslts_pm', rslts_pm)

            

        
        
        
        
        
        """
        self.smu.SetOutput(1, self.chan)
        rslts_wavl = []
        rslts_pwr = []
        for v in self.v_pts:
            self.smu.SetVoltage(v, self.chan)
            if self.visual:
                self.visual = False
                temp1, temp2 = SweepWavelengthSpectrum.instructions(self)
                rslts_wavl.append(temp1)
                rslts_pwr.append(temp2)
                self.visual = True
            else:
                temp1, temp2 = SweepWavelengthSpectrum.instructions(self)
                rslts_wavl.append(temp1)
                rslts_pwr.append(temp2)

        self.results.add('rslts_wavl', rslts_wavl)
        self.results.add('rslts_pwr', rslts_pwr)
        self.results.add('v_pts', self.v_pts)

        if self.visual:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(11, 6))
            legend = []
            for idx, val in enumerate(self.v_pts):
                plt.plot(rslts_wavl[idx], 10*np.log10(rslts_pwr[idx]))
                legend += ['CH'+str(ii)+'_'+str(val) +
                           ' V' for ii, jj in enumerate(self.pm)]
            plt.xlim(min(rslts_wavl[0]), max(rslts_wavl[0]))
            plt.xlabel('Wavelength [nm]')
            plt.ylabel('Optical Power [dBm]')
            plt.legend(legend)
            plt.title(
                f"Result of Wavelength Spectrum Sweep.\nLaser power: {self.tls.GetPwr()} {self.tls.GetPwrUnit()}")
            plt.tight_layout()

        if self.verbose:
            print("\n***Sequence executed successfully.***")
        return rslts_wavl, rslts_pwr, self.v_pts

        """

