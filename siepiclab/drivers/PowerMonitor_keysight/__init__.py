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
        self.SetPwrUnit(str(state['PwrUnit']), confirm=True)
        self.SetWavl(state['wavl'], confirm=True)

    def GetPwrUnit(self):
        """
        Get the unit setting in the instrument.

        Returns
        -------
        unit : String
            Unit setting of the instrument.
                0: dBm
                1: Watts

        """
        re = self.query('SENS', ':POW:UNIT?')
        unit = int(str(re.strip()))
        return unit

    def SetPwrUnit(self, unit=1, confirm=False, wait=False):
        """
        Set the unit setting in the instrument.

        Parameters
        ----------
        unit : String, optional
            The power unit to set. 0 for dBm, 1 for mW. The defautlt is 1 (mW).
        confirm : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        valid_units = ['0', '1']
        if unit not in valid_units:
            print('ERR: Not a valid unit. Valid units are 0 and 1, as str.')

        self.write('SENS', ':POW:UNIT '+str(unit))

        if wait or confirm:
            self.wait()
        if confirm:
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

    def SetWavl(self, wavl, confirm=False, wait=False):
        """
        Set the wavelength setting in the instrument.

        Parameters
        ----------
        wavl : float
            Wavelength to set the instrument at.
        confirm : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None unless confirm is True.

        """
        self.write('SENS', ':POW:WAV '+str(wavl*1e9)+'NM')

        if wait or confirm:
            self.wait()
        if confirm:
            return(self.GetWavl())

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
            pwr = 10*np.log10(1e3*float(str(re.strip())))
            return pwr
        else:
            pwr = 1e3*float(str(re.strip()))
        return pwr
