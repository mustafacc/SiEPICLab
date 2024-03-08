"""
SiEPIClab instrument driver.

Instrument driver for the Agilent 86140 Series Optical Spectrum Analyzer.

Davin Birdi, Dream Photonics, 2023

Thank you:
@original author: Hossam Shoman, 2018 
Mustafa Hammood
"""
import numpy as np


from siepiclab import instruments

class osa_agilent(instruments.instr_VISA):
    """
    HP-Agilent-Keysight OSA class.

    Includes:
        86142B
    """

    def __init__(self, addr, chan=None):
        super().__init__(addr, chan)

    def reset(self):
        self.query("*rst;*opc?")

    def SingleSweep(self): # does a single sweep
        self.write('INIT:imm')

    def SweepMode(self, single=True):
        return self.query('INIT:CONT?')
        

    def SetSweepMode(self, single=True):
        if single:
            self.write('INIT:CONT:OFF')
        else:
            self.write('INIT:CONT:ON')
    

    def StartWavelength(self):
        self.write("sens:wav:star?")
    
    def SetStartWavelength(self, wavl):
        self.write(f"sens:wav:star {wavl}nm")

    def WavlCenter(self):
        return float(self.query("sens:wav:cent?"))

    def SetWavlCenter(self, wavl):
        self.write(f"sens:wav:cent {wavl}nm")

    def WavlSpan(self):
        return float(self.query("sens:wav:span?"))

    def SetWavlSpan(self, span):
        self.write(f"sens:wav:span {span}nm")

    # LowPriorityTodo
    # def setPoints(self, points):
    #    a.query('trac:poin? tra'))

    """
    TRACE Subsystem Commands:
    A TRACe or a DATA area is a named entity stored in instrument memory.
    """

    def getTraceRange(self):
        start = float(self.query("trac:x:star? tra"))
        stop =  float(self.query("trac:x:stop? tra"))
        return [start, stop]
    
    def getTracePoints(self):
        return int(self.query('trac:poin? tra'))

    def getPower(self):
        self.write('form: ascii')
        pwr_ascii = self.query('trac:data:y? tra').split(',')
        pwr = np.array(pwr_ascii, dtype=np.float32)
        return pwr

    def getWavl(self):
        [start, stop] = self.getTraceRange()
        pts = self.getTracePoints()
        return np.linspace(start, stop, pts, endpoint=True)
    
    def getTrace(self):
        """ 
        ## Gets OSA Trace without sending sweep command
        
        Parameters:
        - (None)
        
        Returns:
        - (np.ndarray) wavl [nm]
        - (np.ndarray) pwr  [dB]
        
        """
        pwr = self.getPower()
        wavl = self.getWavl()
        return wavl, pwr
