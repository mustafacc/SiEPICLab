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

    def __init__(self, single_chan=True):

        self.single_chan = single_chan  # Flag to set to False in case your unit somehow has 2 channels??

    def GetState(self):
        """Return an instance of the instrument."""
        currState = instruments.state()
        currState.AddState('output_a', self.GetOutput('A'))
        currState.AddState('volt_a', self.GetVoltage('A'))
        currState.AddState('curr_a', self.GetCurrent('A'))
        currState.AddState('curr_lim_a', self.GetCurrentLimit('A'))
        currState.AddState('volt_lim_a', self.GetVoltageLimit('A'))
        currState.AddState('res_a', self.GetResistance('A'))

        if not self.single_chan:
            currState.AddState('output_b', self.GetOutput('B'))
            currState.AddState('volt_b', self.GetVoltage('B'))
            currState.AddState('curr_b', self.GetCurrent('B'))
            currState.AddState('curr_lim_b', self.GetCurrentLimit('B'))
            currState.AddState('volt_lim_b', self.GetVoltageLimit('B'))
            currState.AddState('res_b', self.GetResistance('B'))
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

        if not self.single_chan:
            self.SetOutput(state['output_b'], 'B', verbose=True)
            self.SetVoltage(state['volt_b'], 'B', verbose=True)
            self.SetCurrent(state['curr_b'], 'B', verbose=True)
            self.SetCurrentLimit(state['curr_lim_b'], 'B', verbose=True)
            self.SetVoltageLimit(state['volt_lim_b'], 'B', verbose=True)

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

    def GetOutput(self, chan):
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
        if chan == 'B':
            status = int(float(self.addr.query(":OUTP2?")))
            return status
        if chan == 'AB':
            status_a = int(float(self.addr.query(":OUTP1?")))
            status_b = int(float(self.addr.query(":OUTP2?")))
            return status_a, status_b

    def SetOutput(self, status, chan, verbose=False, wait=False):
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

        if chan == 'B':
            self.addr.write(f":OUTP2 {status}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetOutput(chan))

        if chan == 'AB':
            self.addr.write(f":OUTP1 {status}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetOutput('A'))

            self.addr.write(f":OUTP2 {status}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetOutput('B'))

    def GetVoltage(self, chan):
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
            volt = float(self.addr.query("SENS1:VOLT?"))
            return volt
        if chan == 'B':
            volt = float(self.addr.query("SENS2:VOLT?"))
            return volt
        if chan == 'AB':
            volt_a = float(self.addr.query("SENS1:VOLT?"))
            volt_b = float(self.addr.query("SENS2:VOLT?"))
            return volt_a, volt_b

    def SetVoltage(self, volt, chan, verbose=False, wait=False):
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

        if chan == 'B':
            self.addr.write(f"SOUR2:VOLT {volt}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltage(chan))

        if chan == 'AB':
            self.addr.write(f"SOUR1:VOLT {volt}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltage('A'))

            self.addr.write(f"SOUR2:VOLT {volt}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltage('B'))

    def GetCurrent(self, chan):
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
            curr = float(self.addr.query("SENS1:CURR?"))
            return curr
        if chan == 'B':
            curr = float(self.addr.query("SENS2:CURR?"))
            return curr
        if chan == 'AB':
            curr_a = float(self.addr.query("SENS1:CURR?"))
            curr_b = float(self.addr.query("SENS2:CURR?"))
            return curr_a, curr_b

    def SetCurrent(self, curr, chan, verbose=False, wait=False):
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

        if chan == 'B':
            self.addr.write(f"SOUR2:CURR {curr}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrent(chan))

        if chan == 'AB':
            self.addr.write(f"SOUR1:CURR {curr}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrent('A'))

            self.addr.write(f"SOUR2:CURR {curr}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrent('B'))

    def GetCurrentLimit(self, chan):
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
        if chan == 'B':
            curr_lim = float(self.addr.query("SENS2:CURR:PROT?"))
            return curr_lim
        if chan == 'AB':
            curr_lim_a = float(self.addr.query("SENS1:CURR:PROT?"))
            curr_lim_b = float(self.addr.query("SENS2:CURR:PROT?"))
            return curr_lim_a, curr_lim_b

    def SetCurrentLimit(self, curr_lim, chan, verbose=False, wait=False):
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

        if chan == 'B':
            self.addr.write(f"SENS2:CURR:PROT {curr_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrentLimit('B'))

        if chan == 'AB':
            self.addr.write(f"SENS1:CURR:PROT {curr_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrentLimit('A'))

            self.addr.write(f"SENS2:CURR:PROT {curr_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrentLimit('B'))

    def GetVoltageLimit(self, chan):
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
        if chan == 'B':
            volt_lim = float(self.addr.query("SENS2:VOLT:PROT?"))
            return volt_lim
        if chan == 'AB':
            volt_lim_a = float(self.addr.query("SENS1:VOLT:PROT?"))
            volt_lim_b = float(self.addr.query("SENS2:VOLT:PROT?"))
            return volt_lim_a, volt_lim_b

    def SetVoltageLimit(self, volt_lim, chan, verbose=False, wait=False):
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

        if chan == 'B':
            self.addr.write(f"SENS2:VOLT:PROT {volt_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltageLimit('B'))

        if chan == 'AB':
            self.addr.write(f"SENS1:VOLT:PROT {volt_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltageLimit('A'))

            self.addr.write(f"SENS2:VOLT:PROT {volt_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltageLimit('B'))

    def GetResistance(self, chan):
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
            res = float(self.addr.query("SENS1:RES?"))
            return res
        if chan == 'B':
            res = float(self.addr.query("SENS2:RES?"))
            return res
        if chan == 'AB':
            res_a = float(self.addr.query("SENS1:RES?"))
            res_b = float(self.addr.query("SENS2:RES?"))
            return res_a, res_b
