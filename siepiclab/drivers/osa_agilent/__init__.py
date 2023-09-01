"""
SiEPIClab instrument driver.

Instrument driver for the Agilent 86140 Series Optical Spectrum Analyzer.

Davin Birdi, Dream Photonics, 2023

Thank you:
@original author: Hossam Shoman, 2018 
Mustafa Hammood
"""


from siepiclab import instruments

class osa_agilent(instruments.instr_VISA):
    """
    HP-Agilent-Keysight OSA class.

    Includes:
        86142B
    """

    def __init__(self, addr, chan=None):
        super().__init__(addr, chan)

    def SingleSweep(self): # does a single sweep
        self.write('INIT')


    def SetSweepMode(self, single=True):
        self.query()

    @property
    def StartWavelength(self):
        return self.query("sens:wav:star?")
    
    @StartWavelength.setter
    def set_StartWavelength(self, wavl):
        self.write(f"sens:wav:star {wavl}nm")


    def reset(self):
        self.query("*rst;*opc?")

    def getPower(self): # set the Yscale dB/div
        PWR=self.query('LDATA')
        PWR=str(PWR) # convert from unicode to string
        PWR=PWR.split(',') # split at the delimiter and set as list
        last=PWR[len(PWR)-1] # select the last element
        last=last[:len(last)-2] # remove the last two characters in the string
        #last=np.asarray(last) # convert the last element to array
        PWR.pop(0) # remove first element
        PWR.pop() # remove last element
        #PWR=np.asarray(PWR) # convert to array
        PWR=np.append(PWR,last)
        PWR=map(float,PWR) # map the strings in the list to float
        PWR=np.array(PWR) # convert to array
        PWR=np.where(PWR==-210.0, -np.inf, PWR)
        return PWR
