"""
SiEPIClab measurement sequence.

Switch sweep sequence. While toggling through a range, run multiple experiments via different optical paths.

Davin Birdi, UBC Photonics

With Templates from:
Mustafa Hammood, SiEPIC Kits, 2022
"""

from siepiclab.sequences.SweepPolarization import SweepPolarization
from siepiclab.sequences.SweepWavelengthSpectrum import SweepWavelengthSpectrum
from siepiclab.sequences.SwitchPath import SwitchPath
from siepiclab import measurements


class SwitchSequences(measurements.sequence):
    """
    Switch Sequences:
    -----------------
    Polarization Optimization:
        
    Wavelength Sweep:
    - 

    """ 
    def __init__(self, tls, pm, pol, mf, sw,  verbose=False, visual=False, saveplot=False):
        super().__init__(self)

        self.tls = tls
        self.pm = pm
        self.pol = pol
        self.mf = mf
        self.jds = sw

        self.instruments.extend([tls, pm, pol, mf, sw])

        self.range = [1,2]
        self.devlist = {
            'device1': 1,
            'device2': 2
        }
        
        # Initialize all the Options. This can be done better with properties and cycling through a list/dictionary        
        self.verbose = verbose
        self.visual = visual
        self.saveplot = saveplot
        self.pause_before_execution = False


        self.Polarization = True
        if self.Polarization:
            self.seq_polopt = SweepPolarization(tls, pol, pm)
            self.seq_polopt.optimize = True
            self.seq_polopt.verbose = self.verbose
            self.seq_polopt.visual = self.visual
            self.seq_polopt.saveplot = self.saveplot
            self.seq_polopt.reset_after_execution = False

        self.WLSweep = True
        if self.WLSweep:
            self.seq_wlsweep = SweepWavelengthSpectrum(mf, tls, pm, mode='step')
            self.seq_wlsweep.verbose = self.verbose  # turn on verbose logging mode
            self.seq_wlsweep.visual = self.visual  # visualize the wavelength sweep results
            self.seq_wlsweep.saveplot = self.saveplot
    
            

        self.experiment = measurements.lab_setup(self.instruments)

    def InstrSetting(self):
        pass

    def instructions(self):
        
        """Instructions of the sequence."""
        
        if self.verbose:
            print("\n***Sequence Starting...***")


        rslts_maxT = []
        rslts_minT = []

        rslts_wavl = []
        rslts_pwr = []

        file_name = self.file_name

        for device_name, chan in self.devlist.items():
            self.chan = chan
            self.dev_name = device_name
            self.file_name = str(file_name) + '_dev' + str(self.dev_name) + '_chan' + str(self.chan)
            if self.verbose:
                print("\n***Switch Changing...***")
            SwitchPath.instructions(self)
            
            # Quickfix for Manual Polarization Optimization
            if self.pause_before_execution:
                self.tls.SetOutput(True)
                while input(f'Press Y to start Sequences on Chan: {self.chan}').lower() != 'y':
                    pass
                self.tls.SetOutput(False)

            if self.Polarization:
                if self.verbose:
                    print(f"\n***Optimizing Polarization on device: {self.dev_name}...***")
                self.seq_polopt.file_name = self.file_name
                self.seq_polopt.execute()
            
                maxT = self.seq_polopt.results.data['maxT']
                minT = self.seq_polopt.results.data['minT']
                rslts_maxT.append(maxT)
                rslts_minT.append(minT)

            if self.WLSweep:
                if self.verbose:
                    print(f"\n*** Performing Wavelength Sweep on device: {self.dev_name}...***")
                self.seq_wlsweep.file_name = self.file_name
                self.seq_wlsweep.execute()
                wavl = self.seq_wlsweep.results.data['rslts_wavl']
                pwr  = self.seq_wlsweep.results.data['rslts_pwr']
                self.results.add('wlsweep' + '-chan' + str(self.chan), [ wavl, pwr ])
                
               

            pass

        # Reset the Filename to it's original after appending 
        self.file_name = file_name

        self.results.add('rslts_maxT', rslts_maxT)
        self.results.add('rslts_minT', rslts_minT)

        
            


        
        
        
        

    