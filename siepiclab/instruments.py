# -*- coding: utf-8 -*-
"""
SiEPIClab instruments module.

Mustafa Hammood, SiEPIC Kits, 2022
"""


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

    def GetState(self):
        """Get the instrument state."""
        return self.state


class instr_VISA(instr):
    """
    VISA instrument class.

    Methods
    -------
    identify
    wait
    query
    write
    """

    def __init__(self, addr, chan=None):
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
        cmd1 : string
            First command.
        cmd2 : string, optional
            second command. The default is ''.

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
        cmd1 : string
            First command.
        cmd2 : string, optional
            second command. The default is ''.

        Returns
        -------
        None.

        """
        if self.chan:
            self.addr.write(cmd1+self.chan+cmd2)
        else:
            self.addr.write(cmd1+cmd2)
