"""
SiEPIClab instrument driver.

Instrument driver for the Keithley 2400 class source measure unit.

Mustafa Hammood, SiEPIC Kits, 2022
"""

from siepiclab import instruments


class smu_keithley2400(instruments.instr_VISA):
    """
    Keithley class source measure unit class.

    Includes:
        Keithley 2400
    """

    def GetState(self):
        """Return an instance of the instrument."""
        currState = instruments.state()
        currState.AddState('output_a', self.GetOutput('A'))
        currState.AddState('volt_a', self.GetVoltage('A'))
        currState.AddState('curr_a', self.GetCurrent('A'))
        currState.AddState('curr_lim_a', self.GetCurrentLimit('A'))
        currState.AddState('volt_lim_a', self.GetVoltageLimit('A'))
        currState.AddState('res_a', self.GetResistance('A'))

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
        self.SetOutput(state['output_a'], 'A', verbose=True)
        self.SetVoltage(state['volt_a'], 'A', verbose=True)
        self.SetCurrent(state['curr_a'], 'A', verbose=True)
        self.SetCurrentLimit(state['curr_lim_a'], 'A', verbose=True)
        self.SetVoltageLimit(state['volt_lim_a'], 'A', verbose=True)

    def reset(self, verbose=False):
        """
        Reset the instrument.

        A good practice is to reset the instrument to its default settings
            before the start of a test.
        """
        self.addr.write(":STAT:QUEUE:CLEAR")
        self.addr.write("*RST")
        self.addr.write(":STAT:PRES")
        self.addr.write(":*CLS")
        if verbose:
            print('Reseting the Keithley Source Measure Unit instrument. . .')

    def SetVoltageMode(self, chan='A', verbose=False, wait=False):
        """
        Set the instrument to measure voltage.

        Returns
        -------
        None.

        """
        if chan == 'A':
            self.addr.write("SOUR1:FUNC CURR")
            self.addr.write("SOUR1:CURR 0")
            self.addr.write("CONF:VOLT")
            self.addr.write("FORM:ELEM VOLT")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.addr.query('CONF?'))

    def SetCurrentMode(self, chan='A', verbose=False, wait=False):
        """
        Set the instrument to measure current.

        Returns
        -------
        None.

        """
        if chan == 'A':
            self.addr.write("SOUR1:FUNC VOLT")
            self.addr.write("SOUR1:VOLT 0")
            self.addr.write("CONF:CURR")
            self.addr.write("FORM:ELEM CURR")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.addr.query('CONF?'))

    def SetResistanceMode(self, chan='A', verbose=False, wait=False):
        """
        Set the instrument to measure resistance.

        Returns
        -------
        None.

        """
        if chan == 'A':
            self.addr.write("CONF:RES")
            self.addr.write("FORM:ELEM RES")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.addr.query('CONF?'))

    def GetOutput(self, chan='A'):
        """
        Get the state of the input/output channel (turned on or off).

        Parameters
        ----------
        chan : String
            Source measure unit channel. "A" or "B".

        Returns
        -------
        status : Boolean
            State of the power output.
                True: source is turned on.
                False: source is turned off.

        """
        if chan == 'A':
            try:
                status = int(float(self.addr.query(":OUTP1?")))
            except ValueError:
                status = 0
            return status

    def SetOutput(self, status, chan='A', verbose=False, wait=False):
        """
        Set the state of the input/output channel (turned on or off).

        Parameters
        ----------
        status : Boolean
            State of the power output.
                True: channel is turned on.
                False: channel is turned off.
        chan : String
            Source measure unit channel. "A" or "B".
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        if chan == 'A':
            self.addr.write(f":OUTP1 {status}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetOutput(chan))

    def GetVoltage(self, chan='A'):
        """
        Get the channel voltage.

        Parameters
        ----------
        chan : String
            Source measure unit channel. "A" or "B".

        Returns
        -------
        volt : float
            Measured voltage at the channel (V)

        """
        if chan == 'A':
            self.SetVoltageMode(chan)
            volt = float(self.addr.query("READ?"))
            return volt

    def SetVoltage(self, volt, chan='A', verbose=False, wait=False):
        """
        Set the voltage of the output channel.

        Parameters
        ----------
        volt : Float
            Voltage of the channel (V).
        chan : String
            Source measure unit channel. "A" or "B".
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        if chan == 'A':
            self.addr.write(f"SOUR1:VOLT {volt}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltage(chan))

    def GetCurrent(self, chan='A'):
        """
        Get the channel current.

        Parameters
        ----------
        chan : String
            Source measure unit channel. "A" or "B".

        Returns
        -------
        curr : float
            Measured current at the channel (A)

        """
        if chan == 'A':
            self.SetVoltageMode(chan)
            curr = float(self.addr.query("READ?"))
            return curr

    def SetCurrent(self, curr, chan='A', verbose=False, wait=False):
        """
        Set the current of the output channel.

        Parameters
        ----------
        curr : Float
            Current of the channel (A).
        chan : String
            Source measure unit channel. "A" or "B".
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        if chan == 'A':
            self.addr.write(f"SOUR1:CURR {curr}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrent(chan))

    def GetCurrentLimit(self, chan='A'):
        """
        Get the channel current compliance (limit) setting.

        Parameters
        ----------
        chan : String
            Source measure unit channel. "A" or "B".

        Returns
        -------
        curr_lim : float
            Setting of the current compliance at the channel (A).

        """
        if chan == 'A':
            curr_lim = float(self.addr.query("SENS1:CURR:PROT?"))
            return curr_lim

    def SetCurrentLimit(self, curr_lim, chan='A', verbose=False, wait=False):
        """
        Set the current compliance (limit) of the output channel.

        Parameters
        ----------
        curr_lim : Float
            Current compliance setting of the channel (A).
        chan : String
            Source measure unit channel. "A" or "B".
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        if chan == 'A':
            self.addr.write(f"SENS1:CURR:PROT {curr_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrentLimit('A'))

    def GetVoltageLimit(self, chan='A'):
        """
        Get the channel voltage compliance (limit) setting.

        Parameters
        ----------
        chan : String
            Source measure unit channel. "A" or "B".

        Returns
        -------
        volt_lim : float
            Setting of the voltage compliance at the channel (V).

        """
        if chan == 'A':
            volt_lim = float(self.addr.query("SENS1:VOLT:PROT?"))
            return volt_lim

    def SetVoltageLimit(self, volt_lim, chan='A', verbose=False, wait=False):
        """
        Set the voltage compliance (limit) of the output channel.

        Parameters
        ----------
        volt_lim : Float
            Voltage compliance setting of the channel (V).
        chan : String
            Source measure unit channel. "A" or "B".
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        if chan == 'A':
            self.addr.write(f"SENS1:VOLT:PROT {volt_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltageLimit('A'))

    def GetResistance(self, chan='A'):
        """
        Get the channel resistance.

        Parameters
        ----------
        chan : String
            Source measure unit channel. "A" or "B".

        Returns
        -------
        res : float
            Measured resistance at the channel (Ohms)

        """
        if chan == 'A':
            self.SetResistanceMode(chan)
            res = float(self.addr.query("READ?"))
            return res
