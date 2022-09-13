"""
SiEPIClab measurement sequence.

Switch sweep sequence. While toggling through a range, run multiple experiments via different optical paths.

Davin Birdi, UBC Photonics

With Templates from:
Mustafa Hammood, SiEPIC Kits, 2022
"""
from SweepPolarization import SweepPolarization
from SweepWavelengthSpectrum import SweepWavelengthSpectrum
from SwitchPath import SwitchPath
from siepiclab import measurements


class SwitchSequences(measurements.sequence): 
    def __init__(self, tls, pm, mf, sw,  verbose=False, visual=False, saveplot=False):
#    def __init__(self, tls, pm, pol, mf, sw,  verbose=False, visual=False, saveplot=False):
        super().__init__(self)

        #SweepWavelengthSpectrum.__init__(self, mf, tls, pm, mode='step')


        self.tls = tls
        self.pm = pm
#        self.pol = pol
        self.mf = mf
        self.jds = sw

        self.instruments.extend([tls, pm, mf, sw])

        self.range = [1,2]
        
        # Initialize all the Options. This can be done better with properties and cycling through a list/dictionary        
        self.verbose = verbose
        self.visual = visual
        self.saveplot = saveplot
        self.pause_before_execution = False


        self.Polarization = False
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

        for i in self.range:
            self.chan = i
            self.file_name = str(file_name) + '-chan' + str(self.chan)
            if self.verbose:
                print("\n***Switch Changing...***")
            SwitchPath.instructions(self)
            
            # Quickfix for Manual Polarization Optimization
            self.tls.SetOutput(True)
            while input(f'Press Y to start Sequences on Chan: {self.chan}').lower() != 'y':
                pass
            self.tls.SetOutput(False)

            if self.Polarization:
                if self.verbose:
                    print("\n***Optimizing Polarization...***")
                self.seq_polopt.execute()
            
                maxT = self.seq_polopt.results.data['maxT']
                minT = self.seq_polopt.results.data['minT']
                rslts_maxT.append(maxT)
                rslts_minT.append(minT)

            if self.WLSweep:
                if self.verbose:
                    print("\n*** Performing Wavelength Sweep...***")
                self.seq_wlsweep.file_name = self.file_name
                self.seq_wlsweep.execute()
                wavl = self.seq_wlsweep.results.data['rslts_wavl']
                pwr  = self.seq_wlsweep.results.data['rslts_pwr']
                self.results.add('wlsweep' + '-chan' + str(self.chan), [ wavl, pwr  ])

            pass

        self.file_name = file_name
        self.results.add('rslts_maxT', rslts_maxT)
        self.results.add('rslts_minT', rslts_minT)

        
            


        
        
        
        

    