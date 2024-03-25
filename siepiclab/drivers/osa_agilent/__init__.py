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

    def SingleSweep(self, timeout_safety=6):
        """
        does a single sweep
        timeout_safety corresponds to 
        """
        import time
        self.write('syst:comm:gpib:buff on')
        self.write('sens:swe:time:auto on')
        timeout = self.GetSweepTime()+timeout_safety
        # Runs the Sweep:
        self.addr.write('init:imm')
        # Ensures no other GPIB Commands are run until the previous commands are finished.
        self.addr.write('wai')
        time.sleep(timeout)


    def GetSweepTime(self):
        return float(self.addr.query('SENS:SWE:TIME?').strip())

    def SweepMode(self, single=True):
        return self.addr.query('INIT:CONT?')
        

    def SetSweepMode(self, single=True):
        if single:
            self.write('INIT:CONT:OFF')
        else:
            self.write('INIT:CONT:ON')
    

    def StartWavelength(self):
        self.write("sens:wav:star?")
    
    def SetStartWavelength(self, wavl):
        self.write(f"sens:wav:star {wavl}nm")

    def SetSensitivity(self, sens):
        """input in dBm"""
        self.write(f'sens:pow:DC:RANG:LOW {sens}dbm')
        pass

    def SetReference(self, lvl):
        self.write(f"DISP:WIND:TRAC:Y:SCAL:RLEV {lvl}dbm")
        pass

    def SetResolution(self, res=None):
        if res == None:
            self.write('sens:band:res:AUTO ON')
        else:
            self.write('sens:band:res:AUTO OFF')
            self.write(f'sens:band:res {res}nm')

    def WavlCenter(self):
        return float(self.query("sens:wav:cent?"))

    def SetWavlCenter(self, wavl):
        """units in nm."""
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
        start = float(self.addr.query("trac:x:star? tra"))
        stop =  float(self.addr.query("trac:x:stop? tra"))
        return [start, stop]
    
    def getTracePoints(self):
        return int(self.addr.query('trac:poin? tra'))

    def getPower(self):
        #self.write('form: ascii')
        pwr_ascii = self.addr.query('trac:data:y? tra').split(',')
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
