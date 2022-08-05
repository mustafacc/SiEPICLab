"""
SiEPIClab instrument driver.

Instrument driver for the HP-Agilent-Keysight Lightwave Measurement System Mainframe

Mustafa Hammood, SiEPIC Kits, 2022
"""

from siepiclab import instruments


class lwmm_keysight(instruments.instr_VISA):
    """
    HP-Agilent-Keysight Lightwave Measurement System Mainframe class.

    Includes:
        8164A
    """

    def GetState(self):
        """Return an instance of the instrument."""
        currState = instruments.state()
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
        return 0
