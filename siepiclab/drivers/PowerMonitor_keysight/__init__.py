"""
SiEPIClab instrument driver.

Instrument driver for the HP-Agilent-Keysight PowerMonitor_keysight instruments.

Mustafa Hammood, SiEPIC Kits, 2022
"""

from siepiclab import instruments
import numpy as np


class PowerMonitor_keysight(instruments.instr_VISA):
    """
    HP-Agilent-Keysight PowerMonitor_keysight class.

    Includes:
        81635A
        N77
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
        currState.AddState('PwrUnit', self.GetPwrUnit())
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
        self.SetPwrUnit(str(state['PwrUnit']), verbose=True)
        self.SetWavl(state['wavl'], verbose=True)

    def GetPwr(self, log=False):
        """
        Get the measured power at the optical power meter.

        Parameters
        ----------
        log : Boolean, optional
            Flag to get in log (dBm) or linear (mW). The default is mW.

        Returns
        -------
        pwr : float
            Measured power at the detector (in selected unit).

        """
        re = self.query(':READ', ':POW?')
        if log:
            pwr = 10*np.log10(1e3*abs(float(str(re.strip()))))
            return pwr
        else:
            pwr = 1e3*float(str(re.strip()))
        return pwr

    def GetZeroAll(self):
        """
        Get the zero status for the power detector. If error nonzero is returned.

        Returns
        -------
        zero : int
            Zero flag. Must be zero if channels are zeroed correctly.

        """
        re = self.addr.query('SENS:CHAN:CORR:COLL:ZERO:ALL?')
        zero = int(re.strip())
        return zero

    def SetZeroAll(self, verbose=False, wait=True):
        """
        Zeros the electrical offsets the power monitor.

        IMPORTASNT: MAKE SURE THAT THE CHANNELS ARE COVERED AND NO SIGNAL IS
        INPUT TO THE OPTICAL POWER MONITOR! Takes a while to run, grab a popcorn.

        Parameters
        ----------
        verbose : TYPE, optional
            DESCRIPTION. The default is False.
        wait : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None, unless verbose.

        """
        self.addr.timeout = 200000  # seconds
        self.addr.write('SENS:CHAN:CORR:COLL:ZERO:ALL')

        if verbose or wait:
            self.wait()
        self.addr.timeout = 2000  # seconds
        if verbose:
            # TODO: returns error VI_ERROR_TMO (-1073807339): Timeout expired.
            # return(self.GetZeroAll())
            return 0

    def GetPwrUnit(self):
        """
        Get the unit setting in the instrument.

        Returns
        -------
        unit : String
            Unit setting of the instrument (mW or dBm).

        """
        re = self.query('SENS', ':POW:UNIT?')
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
        self.write('SENS', ':POW:UNIT '+str(unit))

        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetPwrUnit())

    def GetWavl(self):
        """
        Get the wavelength setting in the instrument.

        Returns
        -------
        wavl : float
            Wavelength setting in the instrument (SI units).

        """
        re = self.query('SENS', ':POW:WAV?')
        wavl = float(str(re.strip()))
        return wavl

    def SetWavl(self, wavl, verbose=False, wait=False):
        """
        Set the wavelength setting in the instrument.

        Parameters
        ----------
        wavl : int
            Wavelength to set the instrument at (nm).
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None unless verbose is True.

        """
        self.write('SENS', ':POW:WAV '+str(int(wavl))+'NM')

        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetWavl())
