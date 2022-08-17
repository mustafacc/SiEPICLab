"""
SiEPIClab instrument driver.

Instrument driver for the JDS S8 Optical Switch (Paired Channel)

Davin Birdi, UBC Photonics

With Credit to:
Mustafa Hammood, SiEPIC Kits, 2022
"""

from pickle import FALSE
from siepiclab import instruments


class opticalSwitch_jds(instruments.instr_VISA):
    """
    JDS S8 Optical Switch Source class.

    Includes:
        GetOpticalPath
        SetOpticalPath
        waitJDS
    """
    
    def GetOpticalPath(self):
        return int(self.addr.query("CLOSE?").strip())

    def SetOpticalPath(self, input, verbose=False):
        if input <= 8 and input >= 0:
            self.addr.write("CLOSE " + str(input))
            self.waitJDS()
        else:
            print("Input larger than 8 or less than 0")

    def waitJDS(self):
        """Blocks the program until the instrument is done with instruction.
           Specific to JDS as it requires no asterisk before the OPC Command"""
        while self.addr.query('OPC?').find('1') == -1:
            pass
    
    
    '''
    @property
    def opticalpath(self):
        return int(self.addr.query("CLOSE?").strip())

    @opticalpath.setter
    def opticalpath(self, input, verbose=FALSE):
        if input <= 8 and input >= 0:
            if verbose:
                print('Sending Write Command:')
            self.addr.write("CLOSE " + str(input))
            
            if verbose:
                print('Send OPC Command')
            self.waitJDS()
        else:
            print("Input larger than 8 or less than 0")
    '''


    def GetState(self):
        """Return an instance of the instrument."""
        currState = instruments.state()
        currState.AddState('output', self.GetOpticalPath())
        #currState.AddState('output', self.opticalpath)
        return currState

    def SetState(self, state):
        """
        Set the state of the instrument to a given state.

        Parameters
        ----------
        state : SiEPIC Lab instruments type
            State of the instrument.

        Returns
        -------
        None.

        """
        self.SetOpticalPath(state['output'], verbose=True)
        pass






    
