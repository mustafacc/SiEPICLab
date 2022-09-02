"""
SiEPIClab measurement sequence.

Wavelength spectrum sweep sequence using tunable laser source and optical power monitor.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements
import time
import numpy as np


class SweepWavelengthSpectrum(measurements.sequence):
    """
    Wavelength spectrum sweep sequence using tunable laser source and optical power monitor.

    Test setup:
        tunable laser -SMF-> ||DUT|| -SMF-> Power Monitor(s)
    
    mode : String, Optional.
        Sets sweep to continous or stepped. Default is continuous.
    verbose : Boolean, Optional.
        Verbose messages and plots flag. Default is False.
    visual : Boolean, Optional.
        Visualization flag. Default is False.
    """

    def __init__(self, mf, tls, pm, mode='CONT'):
        super(SweepWavelengthSpectrum, self).__init__()
        self.mf = mf
        self.tls = tls
        self.pm = pm

        # if user configures only a single power monitor not then make it a list
        if type(self.pm) != list:
            self.pm = [self.pm]

        valid_modes = ['cont', 'step']
        if mode.lower() not in valid_modes:
            TypeError("ERR: Not a valid mode. Valid units are 'cont' and 'step', as str.")
            return

        # sequence default settings
        self.mode = str(mode).lower() # Stepped or Continuous Sweep
        self.pwr = 1  # laser power, mW
        self.sweep_speed = 20  # nm/s
        self.upper_limit = 0  # maximum power expected (dbm, -100: existing setting.)

        if mode == 'step':
            self.wavl_start = 1524  # nm
            self.wavl_stop = 1575  # nm
            self.wavl_pts = 101  # number of points
        else:
            self.wavl_start = 1280  # nm
            self.wavl_stop = 1370  # nm
            self.wavl_pts = 601  # number of points

        self.instruments.extend([mf, tls] + self.pm)
        self.experiment = measurements.lab_setup(self.instruments)

    def setup(self):
        """Instruments setting to customizable sequence parameters."""
        # set the detector to the wavelength and units to mW
        for p in self.pm:
            p.SetWavl(self.wavl)
            p.SetPwrUnit('mW')

        # set the wavelength and power of the laser and turn on
        self.tls.SetWavl(self.wavl)
        self.tls.SetPwrUnit('dBm')
        self.tls.SetPwr(self.pwr)
        self.tls.SetPwrUnit('mW')
        self.tls.SetOutput(True)

        # set tunable laser to send output trigger
        self.tls.write('TRIG', ':OUTP STF')
        # trigger is looped into mainframe
        self.mf.addr.write('TRIG:CONF LOOP')
        # set power meters to receive trigger (also check if there are multiple pms)
        for p in self.pm:
            p.addr.write('TRIG'+str(p.chan)+':INP SME')

        # Configure tunable laser sweep settings
        # sweep mode, cycle number, start wavl, stop wavl, sweep speed, and step
        # set tunable laser mode to continuous sweep
        if self.mode.upper() == 'STEP':
            self.tls.write('SOUR', ':WAV:SWE:MODE STEP')
        else:
            self.tls.write('SOUR', ':WAV:SWE:MODE CONT')
        
        # set tunable laser sweep cycle number to 1
        self.tls.write('SOUR', ':WAV:SWE:CYCL 1')
        self.tls.SetSweepStart(self.wavl_start)
        self.tls.SetSweepStop(self.wavl_stop)
        self.tls.SetSweepSpeed(self.sweep_speed)
        self.tls.SetSweepStep(self.sweep_step)

        for idx, p in enumerate(self.pm):
            p.SetAutoRanging(0)  # disable auto ranging
            p.SetPwrRange(self.upper_limit)
            p.SetPwrUnit('dBm')
            p.SetPwrLoggingPar(self.wavl_pts, 0.5*self.sweep_step/self.sweep_speed)

        self.tls.SetWavlLoggingStatus(True)

    def instructions(self):
        """Instructions of the sequence."""
        if self.verbose:
            print('\nIdentifying instruments . . .')
            for instr in self.instruments:
                print(instr.identify())
            print('\nDone identifying instruments.')

        self.wavl = int((self.wavl_stop+self.wavl_start)/2)
        self.sweep_step = (self.wavl_stop-self.wavl_start)/(self.wavl_pts-1)

        self.setup()
        time_delays = 2.5
        self.tls.SetWavlLoggingStatus(True)
        for p in self.pm:
            p.SetPwrLogging(True)
        time.sleep(time_delays)

        # start the wavelength sweep
        if self.verbose:
            print("***Starting Wavelength Sweep.***")
        self.tls.SetSweepRun(True)
        time.sleep(time_delays)

        while self.tls.GetSweepRun():
            time.sleep(time_delays)  # check every half a sec if the sweep is done
       
        if self.verbose:
            print("***Sweep Finished, fetching.***")
        # fetch the sweep data from the buffers
        if self.mode.upper() == 'STEP':
            # The 81689A cannot log the wavelength (LLOG), hence we infer from our settings.
            rslts_wavl = np.linspace(self.wavl_start, self.wavl_stop, num=self.wavl_pts)
        else:
            rslts_wavl = 1e9*self.tls.GetWavlLoggingData()  # nm

        rslts_pwr = np.zeros((rslts_wavl.size, len(self.pm)))
        for n, p in enumerate(self.pm):
            rslts_pwr[:, n] = 1e3*p.GetPwrLoggingData()  # mW

        # disable power and wavelength logging for power monitor and tunable laser
        for p in self.pm:
            p.SetPwrLogging(False)
            p.SetAutoRanging(1)
            p.addr.write('TRIG'+str(p.chan)+':INP IGN')
        self.tls.SetWavlLoggingStatus(False)
        self.mf.addr.write('TRIG:CONF PASS')

        self.results.add('rslts_wavl', rslts_wavl)
        self.results.add('rslts_pwr', rslts_pwr)

        if self.visual or self.saveplot:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(11, 6))
            plt.plot(rslts_wavl, 10*np.log10(rslts_pwr))
            plt.xlim(min(rslts_wavl), max(rslts_wavl))
            plt.xlabel('Wavelength [nm]')
            plt.ylabel('Optical Power [dBm]')
            plt.legend(['CH'+str(idx) for idx, val in enumerate(self.pm)])
            plt.title(
                f"Result of Wavelength Spectrum Sweep.\nLaser power: {self.tls.GetPwr()} {self.tls.GetPwrUnit()}")
            plt.tight_layout()

            if self.saveplot:
                plt.savefig(str(self.file_name)+ "_wavsweep.png")
                plt.close()
        if self.verbose:
            print("\n***Sequence executed successfully.***")

        return rslts_wavl, rslts_pwr
