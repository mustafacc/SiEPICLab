"""
SiEPIClab instrument driver.

Instrument driver for the HP-Agilent-Keysight tunable laser source instruments.

Mustafa Hammood, SiEPIC Kits, 2022
"""

from siepiclab import instruments
from siepiclab.drivers.fls_keysight import fls_keysight
import numpy as np


class tls_keysight(fls_keysight):
    """
    HP-Agilent-Keysight tunable laser source class.

    Includes:
    """

    def GetState(self):
        """Return an instance of the instrument."""
        currState = instruments.state()
        currState.AddState('output', self.GetOutput())
        currState.AddState('pwr', self.GetPwr())
        currState.AddState('pwr_unit', self.GetPwrUnit())
        currState.AddState('wavl', self.GetWavl())
        currState.AddState('wavl_start', self.GetSweepStart())
        currState.AddState('wavl_stop', self.GetSweepStop())
        currState.AddState('sweep_speed', self.GetSweepSpeed())
        currState.AddState('sweep_step', self.GetSweepStep())
        currState.AddState('wavl_logging', self.GetWavlLoggingStatus())
        currState.AddState('sweep_run', self.GetSweepRun())
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
        self.SetPwrUnit(state['pwr_unit'], verbose=True)
        self.SetWavl(state['wavl'], verbose=True)
        self.SetSweepStart(state['wavl_start'], verbose=True)
        self.SetSweepStop(state['wavl_stop'], verbose=True)
        self.SetSweepSpeed(state['sweep_speed'], verbose=True)
        self.SetSweepStep(state['sweep_step'], verbose=True)
        self.SetWavlLoggingStatus(state['wavl_logging'], verbose=True)
        self.SetSweepRun(state['sweep_run'], verbose=True)

    def GetSweepStart(self):
        """
        Get tunable wavelength sweep start wavelength.

        Returns
        -------
        float
            Wavelength to start wavelength sweep at (in nm)..

        """
        re = self.query('SOUR', ':WAV:SWE:STAR?')
        return 1e9*float(str(re.strip()))

    def SetSweepStart(self, wavl_start, verbose=False, wait=False):
        """
        Set tunable wavelength sweep start wavelength.

        Parameters
        ----------
        wavl_start : float
            Wavelength to start wavelength sweep at (in nm).
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None unless verbose is True.

        """
        self.write('SOUR', ':WAV:SWE:STAR '+str(float(wavl_start))+'NM')
        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetSweepStart())

    def GetSweepStop(self):
        """
        Get tunable wavelength sweep stop wavelength.

        Returns
        -------
        float
            Wavelength to stop wavelength sweep at (in nm)..

        """
        re = self.query('SOUR', ':WAV:SWE:STOP?')
        return 1e9*float(str(re.strip()))

    def SetSweepStop(self, wavl_stop, verbose=False, wait=False):
        """
        Set tunable wavelength sweep stop wavelength.

        Parameters
        ----------
        wavl_start : float
            Wavelength to stop wavelength sweep at (in nm).
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None unless verbose is True.

        """
        self.write('SOUR', ':WAV:SWE:STOP '+str(float(wavl_stop))+'NM')
        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetSweepStop())

    def GetSweepSpeed(self):
        """
        Get tunable wavelength sweep speed.

        Returns
        -------
        float
            Wavelength sweep speed (in nm/s).

        """
        re = self.query('SOUR', ':WAV:SWE:SPE?')
        return 1e9*float(str(re.strip()))

    def SetSweepSpeed(self, sweep_speed, verbose=False, wait=False):
        """
        Set tunable wavelength sweep speed.

        Parameters
        ----------
        sweep_speed : float
            Wavelength sweep speed (in nm/s).
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None unless verbose is True.

        """
        self.write('SOUR', ':WAV:SWE:SPE '+str(sweep_speed)+'nm/s')
        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetSweepSpeed())

    def GetSweepStep(self):
        """
        Get tunable wavelength sweep step.

        Returns
        -------
        float
            Wavelength sweep step (in nm).

        """
        re = self.query('SOUR', ':WAV:SWE:STEP?')
        return 1e9*float(str(re.strip()))

    def SetSweepStep(self, sweep_step, verbose=False, wait=False):
        """
        Set tunable wavelength sweep step.

        Parameters
        ----------
        sweep_speed : float
            Wavelength sweep step (in nm).
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None unless verbose is True.

        """
        self.write('SOUR', ':WAV:SWE:STEP '+str(sweep_step*1e-9))
        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetSweepStep())

    def GetWavlLoggingStatus(self):
        """
        Get wavelength logging status.

        Returns
        -------
        Boolean
            Wavelength logging status.

        """
        re = self.query('SOUR', ':WAV:SWE:LLOG?')
        return int(re.strip()) == 1

    def SetWavlLoggingStatus(self, wavl_logging, verbose=False, wait=False):
        """
        Set wavelength logging status.

        Parameters
        ----------
        wavl_logging : Boolean
            Wavelength logging status.
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None unless verbose is True.

        """
        if wavl_logging:
            self.write('SOUR', ':WAV:SWE:LLOG ON')
        else:
            self.write('SOUR', ':WAV:SWE:LLOG OFF')
        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetWavlLoggingStatus())

    def GetSweepRun(self):
        """
        Get the wavelength sweep status.

        Returns
        -------
        Boolean
            Wavelength sweep running status.
            True: start a sweep.
            False: stop a sweep.

        """
        re = self.query('SOUR', ':WAV:SWE?')
        return int(str(re.strip())) == 1

    def SetSweepRun(self, sweep_run, verbose=False, wait=False):
        """
        Set and control the wavelength sweep status.

        Parameters
        ----------
        sweep_run : Boolean
            Wavelength sweep running status.
            True: start a sweep.
            False: stop a sweep.
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None unless verbose is True.

        """
        if sweep_run:
            self.write('SOUR', ':WAV:SWE STAR')
        else:
            self.write('SOUR', ':WAV:SWE STOP')
        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetSweepRun())

    def GetWavlLoggingData(self):
        """
        Fetch the stored wavelength logging data in the buffer.

        Returns
        -------
        np.array
            Wavelength logging data.

        """
        cmd = 'SOUR'+self.chan+':READ:DATA? LLOG'
        return np.array(self.addr.query_binary_values(cmd, datatype='d', is_big_endian=False))
