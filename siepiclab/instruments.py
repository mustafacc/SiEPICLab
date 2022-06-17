# -*- coding: utf-8 -*-
"""
SiEPIClab instruments module.

Mustafa Hammood, SiEPIC Kits, 2022
"""
import numpy as np


class instr:
    """Instrument abstraction class."""

    def __init__(self):
        return


class state:
    """Instrument state abstraction class."""

    def __init__(self):
        self.state = {}
        return

    def AddState(self, parameter, value):
        """
        Add a state parameter with a given input value to the instrument state.

        Parameters
        ----------
        parameter : ANY TYPE
            Parameter of the state.
        value : ANY TYPE
            Value of the parameter of the state.

        Returns
        -------
        None.

        """
        self.state[parameter] = value


class instr_VISA(instr):
    """
    Instrument class.

    TODO: docs
    Methods
    -------
    identify
    wait
    query
    write
    """

    def __init__(self, addr, chan):
        self.addr = addr
        self.chan = chan

    def identify(self):
        """
        Identify the instrument.

        Returns
        -------
        idn : String
            Instrument VISA identifier.

        """
        idn = self.addr.query('*IDN?').strip()
        return idn

    def wait(self):
        """Blocks the program until the instrument is done with instruction."""
        while self.addr.query('*OPC?').find('1') == -1:
            pass

    def read(self):
        """
        Read a command in the buffer.

        Returns
        -------
        re : String
            Response from the instrument.

        """
        re = self.addr.read()
        return re

    def query(self, cmd1, cmd2=''):
        """
        Ask the instrument and wait for a response.

        Parameters
        ----------
        cmd1 : TYPE
            DESCRIPTION.
        cmd2 : TYPE, optional
            DESCRIPTION. The default is ''.

        Returns
        -------
        None.

        """
        return(self.addr.query(cmd1+self.chan+cmd2))

    def write(self, cmd1, cmd2=''):
        """
        Write a command to the instrument.

        Parameters
        ----------
        cmd1 : TYPE
            DESCRIPTION.
        cmd2 : TYPE, optional
            DESCRIPTION. The default is ''.

        Returns
        -------
        None.

        """
        self.addr.write(cmd1+self.chan+cmd2)


class PowerMonitor_keysight(instr_VISA):
    """
    HP-Agilent-Keysight Power monitor class.

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
            return(instr_VISA.identify(self))

    def GetState(self):
        """Return an instance of the instrument."""
        currState = state()
        currState.AddState('PwrUnit', self.GetPwrUnit())
        currState.AddState('wavl', self.GetWavl())
        return self

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
        self.SetPwrUnit(state['PwrUnit'], confirm=True)
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


class fls_keysight(instr_VISA):
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
            return(instr_VISA.identify(self))


class PolCtrl_keysight(instr_VISA):
    """
    HP-Agilent-Keysight Polarization Controller class.

    Includes:
        11896A
    """

    def GetState(self):
        """Return an instance of the instrument."""
        currState = state()
        currState.AddState('PaddlePositionAll', self.GetPaddlePositionAll())
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
        self.SetPaddlePositionAll(state['PaddlePositionAll'], confirm=True)

    def StartScan(self):
        """Start a random polarization scan."""
        self.write('INIT:IMM')

    def GetPaddlePosition(self, paddle=1):
        """
        Get the position of one paddle in the instrument (of the 3).

        Parameters
        ----------
        paddle : int, optional
            Paddle ID in the instrument. 1,2, and 3 are valid. The default is 1.

        Returns
        -------
        position : int
            Paddle position (value from 0 to 999).

        """
        re = self.addr.query('PADD'+np.str(np.int(paddle))+':POS?')
        position = int(str(re.strip()))
        return position

    def SetPaddlePosition(self, paddle=1, position=500, confirm=False, wait=False):
        """
        Set the position of an given paddle in the instrument.

        Parameters
        ----------
        paddle : int, optional
            Paddle ID in the instrument. 1,2, and 3 are valid. The default is 1.
        position : int
            Paddle position (value from 0 to 999).
        confirm : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        self.addr.write('PADD'+np.str(np.int(paddle)) + ':POS '+np.str(np.int(position)))
        if wait or confirm:
            self.wait()
        if confirm:
            return(self.GetPaddlePosition(paddle))

    def GetPaddlePositionAll(self, numPaddles=4):
        """
        Get all the paddles position in the instrument.

        Parameters
        ----------
        numPaddles : TYPE, optional
            DESCRIPTION. The default is 4.

        Returns
        -------
        paddlePositions : list
            list of ints of each paddle position (each is from 0 to 999).

        """
        paddlePositions = []
        for pad in range(numPaddles):
            paddlePositions.append(self.GetPaddlePosition(pad+1))
        return paddlePositions

    def SetPaddlePositionAll(self, positions=[500, 500, 500, 500], confirm=False, wait=False):
        """
        Set the paddle positions for all paddles in the instruemnt.

        Parameters
        ----------
        positions : [list], optional
            List of ints of the paddles positions. The default is [500, 500, 500, 500].
        confirm : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        for paddle in range(len(positions)):
            self.SetPaddlePosition(paddle+1, positions[paddle])
        if wait or confirm:
            self.wait()
        if confirm:
            return(self.GetPaddlePositionAll())
