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
