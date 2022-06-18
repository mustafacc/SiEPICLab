"""
SiEPIClab instrument driver.

Instrument driver for the HP-Agilent-Keysight fixed laser source instruments.

Mustafa Hammood, SiEPIC Kits, 2022
"""

from siepiclab import instruments


class fls_keysight(instruments.instr_VISA):
    """
    HP-Agilent-Keysight Fixed Laser Source class.

    Includes:
    """

    def identify(self, slot=True):
        """
        Identify the instrument.

        Parameters
        ----------
        slot : Boolean, optional
            Flag if the instrument is a mainframe slot. The default is True.

        Returns
        -------
        Instrument identifier (string).

        """
        if slot:
            return(self.query('SLOT', ':IDN?').strip())
        else:
            return(instruments.instr_VISA.identify(self))

    def GetState(self):
        """Return an instance of the instrument."""
        currState = instruments.state()
        currState.AddState('output', self.GetOutput())
        currState.AddState('pwr', self.GetPwr())
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
        self.SetOutput(state['output'], confirm=True)
        self.SetPwr(state['pwr'], confirm=True)

    def GetPwr(self):
        """
        Get the output power of the laser.

        Returns
        -------
        pwr : float
            Output power of the laser (mW).

        """
        re = self.addr.query('SOUR', ':POW?')
        pwr = float(str(re.strip()))*1e3
        return pwr

    def SetPwr(self, state, confirm=False, wait=False):
        return

    def GetOutput(self):
        """
        Get the state of the laser output power (turned on or off).

        Returns
        -------
        state : Boolean
            State of the power output.
                True: laser is turned on.
                False: laser is turned off.

        """
        re = self.query('SOUR', ':POW:STAT?')
        state = int(str(re.strip()))
        if state == 1:
            state = True
            return state
        else:
            state = False
            return state

    def SetOutput(self, state, confirm=False, wait=False):
        """
        Set the state of the laser output power (turned on or off).

        Parameters
        ----------
        state : Boolean
            State of the power output.
                True: laser is turned on.
                False: laser is turned off.
        confirm : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        if state:
            self.write('SOUR', ':POW:STAT 1')
        else:
            self.write('SOUR', ':POW:STAT 0')

        if wait or confirm:
            self.wait()
        if confirm:
            return(self.GetOutput())
