"""
SiEPIClab instrument driver.

Instrument driver for the HP-Agilent-Keysight tunable laser source instruments.

Mustafa Hammood, SiEPIC Kits, 2022
"""

from siepiclab import instruments

class tls_keysight(instruments.instr_VISA):
    """
    HP-Agilent-Keysight tunable laser source class.

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
        currState.AddState('pwrUnit', self.GetPwrUnit())
        currState.AddState('wavl', self.GetWavl())
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
        self.SetOutput(state['output'], verbose=True)
        self.SetPwr(state['pwr'], verbose=True)
        self.SetPwrUnit(state['pwrUnit'], verbose=True)
        self.SetWavl(state['wavl'], verbose=True)

    def GetPwrUnit(self):
        """
        Get the unit setting in the instrument.

        Returns
        -------
        unit : String
            Unit setting of the instrument (mW or dBm).

        """
        re = self.query('SOUR', ':POW:UNIT?')
        unit = int(str(re.strip()))
        if unit == 1:
            unit = 'mW'
        else:
            unit = 'dBm'
        return unit

    def SetPwrUnit(self, unit='mW', verbose=False, wait=False):
        """
        Set the unit setting in the instrument.

        Parameters
        ----------
        unit : String, optional
            The power unit to set. 'dBm' or 'mW'. The defautlt is 'mW'.
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        valid_units = ['dbm', 'mw']
        if unit.lower() not in valid_units:
            print("ERR: Not a valid unit. Valid units are 'dBm' and 'mW', as str.")
            return
        if unit.lower() == 'dbm':
            unit = 0
        else:
            unit = 1
        self.write('SOUR', ':POW:UNIT '+str(unit))

        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetPwrUnit())

    def GetPwr(self):
        """
        Get the output power of the laser.

        Returns
        -------
        pwr : float
            Output power of the laser (mW).

        """
        re = self.query('SOUR', ':POW?')
        pwr = float(str(re.strip()))*1e3
        return pwr

    def SetPwr(self, pwr, verbose=False, wait=False):
        """
        Set the output power of the laser.

        Parameters
        ----------
        pwr : float
            Output power of the laser (mW).
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        self.write('SOUR', ':POW '+str(pwr)+'mW')

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

    def SetOutput(self, state, verbose=False, wait=False):
        """
        Set the state of the laser output power (turned on or off).

        Parameters
        ----------
        state : Boolean
            State of the power output.
                True: laser is turned on.
                False: laser is turned off.
        verbose : Boolean, optional
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
        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetOutput())

    def GetWavl(self):
        """
        Get the laser wavelength.

        Returns
        -------
        wavl : float
            Wavelength of the laser (nm)

        """
        re = self.query('SOUR', ':WAV?')
        wavl = float(str(re.strip()))*1e9
        return wavl

    def SetWavl(self, wavl, verbose=False, wait=False):
        """
        Set the laser wavelength.

        Parameters
        ----------
        wavl : float
            Wavelength of the laser (nm)
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        self.write('SOUR', ':WAV '+str(wavl)+'NM')
        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetOutput())
