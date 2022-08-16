"""
SiEPIClab measurement sequence.

LDC Setup and current sweep sequence.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements


class SetupLDC501(measurements.sequence):
    """
    Current sweep sequence.
    """

    def __init__(self, ldc):
        self.ldc = ldc

        self.optimize = False
        self.verbose = False
        self.visual = False

        self.instruments = [ldc]
        self.experiment = measurements.lab_setup(self.instruments)

        self.temp=21

    def InstrSetting(self):
        
        
        pass

    def instructions(self):
        self.ldc.SetTemperature(self.temp)
        if(self.verbose):
            print("Turning on the TEC")
        self.ldc.tecON()

        print(self.ldc.GetTemperature())
        #print(self.ldc.GetPDpowerLim())
        pass
        