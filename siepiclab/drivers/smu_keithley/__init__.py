"""
SiEPIClab instrument driver.

Instrument driver for the Keithley class source measure unit.

Mustafa Hammood, SiEPIC Kits, 2022
"""

from siepiclab import instruments


class smu_keithley(instruments.instr_VISA):
    """
    Keithley class source measure unit class.

    Includes:
        Keithley 2602
    """

    def GetState(self):
        """Return an instance of the instrument."""
        currState = instruments.state()
        currState.AddState('output_a', self.GetOutput('A'))
        currState.AddState('output_b', self.GetOutput('B'))
        currState.AddState('volt_a', self.GetVoltage('A'))
        currState.AddState('volt_b', self.GetVoltage('B'))
        currState.AddState('curr_a', self.GetCurrent('A'))
        currState.AddState('curr_b', self.GetCurrent('B'))
        currState.AddState('curr_lim_a', self.GetCurrentLimit('A'))
        currState.AddState('curr_lim_b', self.GetCurrentLimit('B'))
        currState.AddState('volt_lim_a', self.GetVoltageLimit('A'))
        currState.AddState('volt_lim_b', self.GetVoltageLimit('B'))
        currState.AddState('res_a', self.GetResistance('A'))
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
        self.SetOutput(state['output_b'], 'B', verbose=True)
        self.SetVoltage(state['volt_a'], 'A', verbose=True)
        self.SetVoltage(state['volt_b'], 'B', verbose=True)
        self.SetCurrent(state['curr_a'], 'A', verbose=True)
        self.SetCurrent(state['curr_b'], 'B', verbose=True)
        self.SetCurrentLimit(state['curr_lim_a'], 'A', verbose=True)
        self.SetCurrentLimit(state['curr_lim_b'], 'B', verbose=True)
        self.SetVoltageLimit(state['volt_lim_a'], 'A', verbose=True)
        self.SetVoltageLimit(state['volt_lim_b'], 'B', verbose=True)

    def reset(self):
        """
        Reset the instrument.

        A good practice is to reset the instrument to its default settings
            before the start of a test.
        """
        self.addr.write("smua.reset()")
        self.addr.write("smub.reset()")
        print('Reseting the Keithley Source Measure Unit instrument. . .')

    def GetOutput(self, chan):
        if chan == 'A':
            status = int(float(self.addr.query("print(smua.source.output)")))
            return status
        if chan == 'B':
            status = int(float(self.addr.query("print(smub.source.output)")))
            return status
        if chan == 'AB':
            status_a = int(float(self.addr.query("print(smua.source.output)")))
            status_b = int(float(self.addr.query("print(smub.source.output)")))
            return status_a, status_b

    def SetOutput(self, status, chan, verbose=False, wait=False):
        if status == 1:
            status_str = 'OUTPUT_ON'
        elif status == 0:
            status_str = 'OUTPUT_OFF'
        else:
            print("[ERR] Not a valid status. Options are 1:ON and 0:OFF.")
            return
        if chan == 'A':
            self.addr.write(f"smua.source.output =smua.{status_str}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetOutput(chan))

        if chan == 'B':
            self.addr.write(f"smub.source.output =smub.{status_str}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetOutput(chan))

        if chan == 'AB':
            self.addr.write(f"smua.source.output =smua.{status_str}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetOutput('A'))

            self.addr.write(f"smuv.source.output =smuv.{status_str}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetOutput('B'))

    def GetVoltage(self, chan):
        if chan == 'A':
            volt = float(self.addr.query("print(smua.measure.v())"))
            return volt
        if chan == 'B':
            volt = float(self.addr.query("print(smub.measure.v())"))
            return volt
        if chan == 'AB':
            volt_a = float(self.addr.query("print(smua.measure.v())"))
            volt_b = float(self.addr.query("print(smub.measure.v())"))
            return volt_a, volt_b

    def SetVoltage(self, volt, chan, verbose=False, wait=False):
        if chan == 'A':
            self.addr.write("smua.source.func = smua.OUTPUT_DCVOLTS")
            setvoltstring = "smua.source.levelv = " + str(volt)
            self.addr.write(setvoltstring)
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltage(chan))

        if chan == 'B':
            self.addr.write("smub.source.func = smub.OUTPUT_DCVOLTS")
            setvoltstring = "smub.source.levelv = " + str(volt)
            self.addr.write(setvoltstring)
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltage(chan))

        if chan == 'AB':
            self.addr.write("smua.source.func = smua.OUTPUT_DCVOLTS")
            setvoltstring = "smua.source.levelv = " + str(volt)
            self.addr.write(setvoltstring)
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltage('A'))

            self.addr.write("smub.source.func = smub.OUTPUT_DCVOLTS")
            setvoltstring = "smub.source.levelv = " + str(volt)
            self.addr.write(setvoltstring)
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltage('B'))

    def GetCurrent(self, chan):
        if chan == 'A':
            curr = float(self.addr.query("print(smua.measure.i())"))
            return curr
        if chan == 'B':
            curr = float(self.addr.query("print(smub.measure.i())"))
            return curr
        if chan == 'AB':
            curr_a = float(self.addr.query("print(smua.measure.i())"))
            curr_b = float(self.addr.query("print(smub.measure.i())"))
            return curr_a, curr_b

    def SetCurrent(self, curr, chan, verbose=False, wait=False):
        if chan == 'A':
            self.addr.write("smua.source.func = smua.OUTPUT_DCAMPS")
            setcurrentstring = "smua.source.leveli = " + str(curr)
            self.addr.write(setcurrentstring)
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrent('A'))

        if chan == 'B':
            self.addr.write("smub.source.func = smub.OUTPUT_DCAMPS")
            setcurrentstring = "smub.source.leveli = " + str(curr)
            self.addr.write(setcurrentstring)
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrent('B'))

        if chan == 'AB':
            self.addr.write("smua.source.func = smua.OUTPUT_DCAMPS")
            setcurrentstring = "smua.source.leveli = " + str(curr)
            self.addr.write(setcurrentstring)
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrent('A'))

            self.addr.write("smub.source.func = smub.OUTPUT_DCAMPS")
            setcurrentstring = "smub.source.leveli = " + str(curr)
            self.addr.write(setcurrentstring)
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrent('B'))

    def GetCurrentLimit(self, chan):
        if chan == 'A':
            curr = float(self.addr.query("print(smua.source.limiti)"))
            return curr
        if chan == 'B':
            curr = float(self.addr.query("print(smub.source.limiti)"))
            return curr
        if chan == 'AB':
            curr_a = float(self.addr.query("print(smua.source.limiti)"))
            curr_b = float(self.addr.query("print(smub.source.limiti)"))
            return curr_a, curr_b

    def SetCurrentLimit(self, curr_lim, chan, verbose=False, wait=False):
        if chan == 'A':
            self.addr.write(f"smua.source.limiti = {curr_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrentLimit('A'))

        if chan == 'B':
            self.addr.write(f"smub.source.limiti = {curr_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrentLimit('B'))

        if chan == 'AB':
            self.addr.write(f"smua.source.limiti = {curr_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrentLimit('A'))

            self.addr.write(f"smub.source.limiti = {curr_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetCurrentLimit('B'))

    def GetVoltageLimit(self, chan):
        if chan == 'A':
            volt = float(self.addr.query("print(smua.source.limitv)"))
            return volt
        if chan == 'B':
            volt = float(self.addr.query("print(smub.source.limitv)"))
            return volt
        if chan == 'AB':
            volt_a = float(self.addr.query("print(smua.source.limitv)"))
            volt_b = float(self.addr.query("print(smub.source.limitv)"))
            return volt_a, volt_b

    def SetVoltageLimit(self, volt_lim, chan, verbose=False, wait=False):
        if chan == 'A':
            self.addr.write(f"smua.source.limitv = {volt_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltageLimit('A'))

        if chan == 'B':
            self.addr.write(f"smub.source.limitv = {volt_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltageLimit('B'))

        if chan == 'AB':
            self.addr.write(f"smua.source.limitv = {volt_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltageLimit('A'))

            self.addr.write(f"smub.source.limitv = {volt_lim}")
            if wait or verbose:
                self.wait()
            if verbose:
                return(self.GetVoltageLimit('B'))

    def SetPowerLimit(self, pow_lim, chan, verbose=False, wait=False):
        if chan == 'A':
            self.addr.write(f"smua.source.limitp = {pow_lim}")
            if wait or verbose:
                self.wait()

        if chan == 'B':
            self.addr.write(f"smub.source.limitp = {pow_lim}")
            if wait or verbose:
                self.wait()

        if chan == 'AB':
            self.addr.write(f"smua.source.limitp = {pow_lim}")
            if wait or verbose:
                self.wait()

            self.addr.write(f"smub.source.limitp = {pow_lim}")
            if wait or verbose:
                self.wait()

    def GetResistance(self, chan):
        if chan == 'A':
            res = float(self.addr.query("print(smua.measure.r())"))
            return res
        if chan == 'B':
            res = float(self.addr.query("print(smub.measure.r())"))
            return res
        if chan == 'AB':
            res_a = float(self.addr.query("print(smua.measure.r())"))
            res_b = float(self.addr.query("print(smub.measure.r())"))
            return res_a, res_b
