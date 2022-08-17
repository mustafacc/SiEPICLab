"""
SiEPIClab measurement sequence.

Changing Optical Paths of the JDS S8 Switch

Davin Birdi, UBC Photonics, 2022
"""

from siepiclab import measurements
from siepiclab.drivers.opticalSwitch_jds import opticalSwitch_jds

from time import sleep

from random import randint

class SwitchPath(measurements.sequence):
    
    def __init__(self, jds, visual=False, verbose=False, saveplot=False):
        super(SwitchPath, self).__init__(visual, verbose, saveplot)
        
        self.jds = jds
        self.instruments = [jds]
        
        self.experiment = measurements.lab_setup(self.instruments)

    def instructions(self):
        """ Instructions for the sequence """
        print(self.jds.GetOpticalPath())
        #print(self.jds.opticalpath)

        self.jds.SetOpticalPath(randint(1,8))
        #self.jds.opticalpath(randint(1,8))

        sleep(2)
        