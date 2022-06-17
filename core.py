# -*- coding: utf-8 -*-
"""
SiEPIClab core module.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from datetime import datetime


class instruction:
    """
    Instruction class.

    TODO: docs
    Methods
    -------
    getTime
    """

    def __init__(self):
        self.time = self.getTime()

    def getTime(self):
        """Get time at which instruction starting executing."""
        return(datetime.now())


class instr:
    """TODO: docs."""

    x = 1


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
        """Identify the instrument."""
        return(self.addr.query('*IDN?'))

    def wait(self):
        """Blocks the program until the instrument is done with instruction."""
        while self.addr.query('*OPC?').find('1') == -1:
            pass

    def read(self):
        """Read a command in the buffer."""
        return(self.addr.read())

    def query(self, cmd1, cmd2=''):
        """
        TODO: docs.

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
        return(self.addr.query(cmd1+self.channel+cmd2))

    def write(self, cmd1, cmd2=''):
        """
        TODO: docs.

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
        self.addr.write(cmd1+self.channel+cmd2)

"""
    def OutputRead(self):
        ans = self.askCmd('SOUR', ':POW:STAT?')
        return(int(str(ans.strip())) == 1)  # True = power output on

"""


class tls_keysight(instr_VISA):
    """
    HP-Agilent-Keysight tunable lasers family.

    covers:
        81606A, 81607A, 81608A, 81609A, 81602A
    Methods
    --------
    WavlRead
    WavlSet
    PwrRead
    PwrSet
    FreqRead
    FreqSet
    AttenRead
    AttenSet
    RefWavlRead
    RefWavlSet
    ShutterRead
    ShutterSet
    """

    def __init__(self, addr, chan):
        instr_VISA.__init__(self, addr, chan)
