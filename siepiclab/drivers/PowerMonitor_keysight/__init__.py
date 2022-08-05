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

    def __init__(self, addr, chan, slot=None):
        super(PowerMonitor_keysight, self).__init__(addr, chan)
        self.slot = slot

    def identify(self):
        """
        Identify the instrument.

        Returns
        -------
        Instrument identifier (string).

        """
        if self.slot:
            return(self.query('SLOT', ':IDN?').strip())
        else:
            return(instruments.instr_VISA.identify(self))

    def GetState(self):
        """Return an instance of the instrument."""
        currState = instruments.state()
        currState.AddState('wavl', self.GetWavl())
        currState.AddState('auto_range', self.GetAutoRanging())
        currState.AddState('pwr_range', self.GetPwrRange())
        currState.AddState('pwr_unit', self.GetPwrUnit())
        currState.AddState('num_pts', self.GetPwrLoggingPar()[0])
        currState.AddState('avg_time', self.GetPwrLoggingPar()[1])
        currState.AddState('pwr_logging', self.GetPwrLogging())
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
        self.SetWavl(state['wavl'], verbose=True)
        self.SetAutoRanging(state['auto_range'], verbose=True)
        self.SetPwrRange(state['pwr_range'], verbose=True)
        self.SetPwrUnit(state['pwr_unit'], verbose=True)
        self.SetPwrLoggingPar(state['num_pts'], state['avg_time'], verbose=True)
        self.SetPwrLogging(state['pwr_logging'], verbose=True)

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
        if self.slot is not None:
            re = self.addr.query(':FETC'+str(self.chan)+':CHAN'+str(self.slot)+':POW?')
        else:
            re = self.query(':FETC', ':POW?')
        if log:
            pwr = 10*np.log10(1e3*float(str(re.strip())))
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
        if self.slot is not None:
            re = self.addr.query('SENS'+str(self.chan)+':CHAN' +
                                 str(self.slot)+':CORR:COLL:ZERO:ALL?')
        else:
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
        if self.slot is not None:
            self.addr.write('SENS'+str(self.chan)+':CHAN' +
                            str(self.slot)+':CORR:COLL:ZERO:ALL')
        else:
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
        if self.slot is not None:
            re = self.addr.query('SENS'+str(self.chan)+':CHAN'+str(self.slot) + ':POW:UNIT?')
        else:
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
        if self.slot is not None:
            self.addr.write('SENS'+str(self.chan)+':CHAN' +
                            str(self.slot)+':POW:UNIT '+str(unit))
        else:
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
            Wavelength setting in the instrument (in nm).

        """
        if self.slot is not None:
            re = self.addr.query('SENS'+str(self.chan)+':CHAN'+str(self.slot) + ':POW:WAV?')
        else:
            re = self.query('SENS', ':POW:WAV?')
        wavl = 1e9*float(str(re.strip()))
        return wavl

    def SetWavl(self, wavl, verbose=False, wait=False):
        """
        Set the wavelength setting in the instrument.

        Parameters
        ----------
        wavl : float
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
        if self.slot is not None:
            self.addr.write('SENS'+str(self.chan)+':CHAN'+str(self.slot) +
                            ':POW:WAV '+str(float(wavl))+'NM')
        else:
            self.write('SENS', ':POW:WAV '+str(float(wavl))+'NM')

        if wait or verbose:
            self.wait()
        if verbose:
            return self.GetWavl()

    def GetAutoRanging(self):
        """
        Get the auto ranging setting for the power monitor.

        Returns
        -------
        int
            Auto ranging setting.
            0: disabled
            1: enabled

        """
        if self.slot is not None:
            re = self.addr.query('SENS'+str(self.chan)+':CHAN' +
                                 str(self.slot)+':POW:RANG:AUTO?')
        else:
            re = self.query('SENS', ':CHAN'+self.chan+':POW:RANG:AUTO?')
        return int(str(re.strip()))

    def SetAutoRanging(self, auto_range, verbose=False, wait=False):
        """
        Set the auto ranging setting for the power monitor.

        Parameters
        ----------
        auto_range : int
            Auto ranging setting.
            0: disabled
            1: enabled
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None unless verbose is True.

        """
        if self.slot is not None:
            self.addr.write('SENS'+str(self.chan)+':CHAN'+str(self.slot) +
                            ':POW:RANG:AUTO '+str(auto_range))
        else:
            self.write('SENS', ':CHAN'+self.chan+':POW:RANG:AUTO '+str(auto_range))
        if wait or verbose:
            self.wait()
        if verbose:
            return self.GetAutoRanging()

    def GetPwrLogging(self):
        """
        Get power logging status.

        Returns
        -------
        string
            Power logging status.

        """
        if self.slot is not None:
            re = self.addr.query('SENS'+str(self.chan)+':CHAN'+str(self.slot)+':FUNC:STAT?')
        else:
            re = self.query('SENS', ':CHAN'+self.chan+':FUNC:STAT?')
        return str(re.strip())

    def SetPwrLogging(self, pwr_logging, verbose=False, wait=False):
        """
        Set power logging status.

        Parameters
        ----------
        pwr_logging : string
            Power logging status.
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None unless verbose is True.

        """
        if pwr_logging:
            if self.slot is not None:
                self.addr.write('SENS'+str(self.chan)+':CHAN' +
                                str(self.slot)+':FUNC:STAT LOGG,STAR')
            else:
                self.write('SENS', ':CHAN'+self.chan+':FUNC:STAT LOGG,STAR')
        else:
            if self.slot is not None:
                self.addr.write('SENS'+str(self.chan)+':CHAN' +
                                str(self.slot)+':FUNC:STAT LOGG,STOP')
            else:
                self.write('SENS', ':CHAN'+self.chan+':FUNC:STAT LOGG,STOP')
        if pwr_logging and wait:
            while self.GetPwrLogging() != 'LOGGING_STABILITY,COMPLETE':
                pass
        if verbose:
            return self.GetPwrLogging()

    def GetPwrRange(self):
        """
        Get the power range upper limit setting for the power monitor.

        Returns
        -------
        float
            Power range upper limit (in dBm).

        """
        if self.slot is not None:
            re = self.addr.query('SENS'+str(self.chan)+':CHAN'+str(self.slot)+':POW:RANG?')
        else:
            re = self.query('SENS', ':CHAN'+self.chan+':POW:RANG?')
        return float(str(re.strip()))

    def SetPwrRange(self, power_range, verbose=False, wait=False):
        """
        Set the auto ranging setting for the power monitor.

        Parameters
        ----------
        power_range : float
            Power range upper limit (in dBm).
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None unless verbose is True.

        """
        if self.slot is not None:
            self.addr.write('SENS'+str(self.chan)+':CHAN' +
                            str(self.slot)+':POW:RANG '+str(power_range))
        else:
            self.write('SENS', ':CHAN'+self.chan+':POW:RANG '+str(power_range))
        if wait or verbose:
            self.wait()
        if verbose:
            return self.GetPwrRange()

    def GetPwrLoggingPar(self):
        """
        Get Power Logging Paramater (number of points and average time in s).

        Returns
        -------
        tuple (of ints)
            Power logging parr setting.
            (number of points, averaging time in seconds)

        """
        if self.slot is not None:
            re = self.addr.query('SENS'+str(self.chan)+':CHAN' +
                                 str(self.slot)+':FUNC:PAR:LOGG?')
        else:
            re = self.query('SENS', ':CHAN'+self.chan+':FUNC:PAR:LOGG?')
        pwr_logging_par = str(re.strip()).split(',')
        return (int(pwr_logging_par[0]), float(pwr_logging_par[1]))

    def SetPwrLoggingPar(self, num_pts, avg_time, verbose=False, wait=False):
        """
        Set Power Logging Paramater (number of points and average time in s).

        Parameters
        ----------
        num_pts : int
            Number of points.
        avg_time : float
            Averaging time (in seconds).
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None unless verbose is True.

        """
        if self.slot is not None:
            self.addr.write('SENS'+str(self.chan)+':FUNC:PAR:LOGG ' +
                            str(int(num_pts))+','+str(avg_time))
        else:
            self.write('SENS', ':CHAN'+self.chan+':FUNC:PAR:LOGG ' +
                       str(int(num_pts))+','+str(avg_time))
        if wait or verbose:
            self.wait()
        if verbose:
            return self.GetPwrLoggingPar()

    def GetPwrLoggingData(self):
        """
        Fetch the stored power logging data in the buffer.

        Parameters
        ----------
        slot : int
            Power meter slot to fetch the data buffer from.

        Returns
        -------
        np.array
            Power logging data.

        """
        if self.slot is not None:
            cmd = 'SENS'+str(self.chan)+':CHAN'+str(self.slot)+':FUNC:RES?'
        else:
            cmd = 'SENS:CHAN'+self.chan+':FUNC:RES?'
        return np.array(self.addr.query_binary_values(cmd))
