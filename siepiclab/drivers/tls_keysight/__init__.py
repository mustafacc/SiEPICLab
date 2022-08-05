"""
SiEPIClab instrument driver.

Instrument driver for the HP-Agilent-Keysight tunable laser source instruments.

Mustafa Hammood, SiEPIC Kits, 2022
"""

from siepiclab import instruments
import numpy as np


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

    def GetPwrUnit(self):
        """
        Get the unit setting in the instrument.

        Returns
        -------
        unit : String
            Unit setting of the instrument (mW or dBm).

        """
        re = self.query('SOUR', ':POW:UNIT?')
        pwr_unit = int(str(re.strip()))
        if pwr_unit == 1:
            pwr_unit = 'mW'
        else:
            pwr_unit = 'dBm'
        return pwr_unit

    def SetPwrUnit(self, pwr_unit='mW', verbose=False, wait=False):
        """
        Set the unit setting in the instrument.

        Parameters
        ----------
        pwr_unit : String, optional
            The power unit to set. 'dBm' or 'mW'. The defautlt is 'mW'.
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None unless verbose is True.

        """
        valid_units = ['dbm', 'mw']
        if pwr_unit.lower() not in valid_units:
            print("ERR: Not a valid unit. Valid units are 'dBm' and 'mW', as str.")
            return
        if pwr_unit.lower() == 'dbm':
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
        None unless verbose is True.

        """
        self.write('SOUR', ':POW '+str(pwr)+'mW')
        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetPwr())

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
        None unless verbose is True.

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
        None unless verbose is True.

        """
        self.write('SOUR', ':WAV '+str(wavl)+'NM')
        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetWavl())

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
