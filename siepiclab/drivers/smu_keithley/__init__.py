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

    def GetOutputMode(self, chan):
        chan = chan.lower()
        mode = int(float(self.addr.query(f'print(smu{chan}.source.func)').strip()))
        if mode == 1:
            print(f'Output mode of channel {chan.upper()} is Voltage')
        else:
            print(f'Output mode of channel {chan.upper()} is Current')
        return mode

    def SetOutputMode(self, chan, mode='volt', verbose=False, wait=False):
        chan = chan.lower()

        if mode == 'volt':
            self.SetVoltage(0., chan)
        elif mode == 'curr':
            self.SetCurrent(0., chan)
        else:
            print("ERR: Invalid mode selection. Possible inputs = ['volt', 'curr']")
        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetOutputMode(chan))            
        return

    def GetOutput(self, chan):
        if chan == 'A':
            try:
                status = int(float(self.addr.query(
                    "print(smua.source.output)")))
            except ValueError:
                status = 0
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

    def sweep_2CH_VV(self, chan1, chan2, volt_start=0, volt_stop=5, volt_num=10, visualize=True):
        """Set a voltage on CH1 and read curr and voltage on CH1, voltage on CH2."""
        import numpy as np
        import time
        import matplotlib.pyplot as plt
        v_arr = np.linspace(volt_start, volt_stop, volt_num)
        chan1 = chan1.upper()
        chan2 = chan2.upper()
        # reset
        self.reset()
        self.wait()
        # configure channels and bias
        self.SetOutputMode(chan1, 'volt')

        self.SetOutputMode(chan2, 'curr')
        self.SetCurrent(0, chan2)
        # turn on
        self.SetOutput(1, chan1)
        self.SetOutput(1, chan2)
        time.sleep(1)
        # perform IV sweep
        v1 = []
        i1 = []
        v2 = []
        for v in v_arr:
            self.SetVoltage(v, chan1)
            v1.append(self.GetVoltage(chan1))
            v2.append(self.GetVoltage(chan2))
            i1.append(self.GetCurrent(chan1))

        # turn off
        self.SetOutput(0, chan1)
        self.SetOutput(0, chan2)

        if visualize:
            fig, ax1 = plt.subplots()
            ax1.plot(i1, v1, label='CH1', color='blue')
            ax1.set_ylabel('Voltage CH1 (V)', color='blue')
            ax1.set_xlabel('Current CH1 (A)', color='blue')

            ax2 = ax1.twinx()
            ax2.plot(i1, v2, label='CH2', color='red')
            ax2.set_ylabel('Voltage CH2 (V)', color='red')
            ax2.set_xlabel('Current CH1 (A)', color='red')

            ax2.set_xlim(ax1.get_xlim())
            ax2.set_ylim(ax1.get_ylim())
            
            ax1.set_title(f'sweep_2CH_VV. CH1= {chan1} - CH2 = {chan2}')
            fig.show()
        return v1, i1, v2

    def sweep_2CH_IV(self, chan1='A', chan2='B', curr_start=0, curr_stop=10e-6, curr_num=10, visualize=True):
        """Set a current on CH1 and read curr and voltage on CH1, voltage on CH2."""
        import numpy as np
        import time
        import matplotlib.pyplot as plt
        i_arr = np.linspace(curr_start, curr_stop, curr_num)
        chan1 = chan1.upper()
        chan2 = chan2.upper()
        # reset
        self.reset()
        self.wait()
        # configure channels and bias
        self.SetOutputMode(chan2, 'curr')

        self.SetOutputMode(chan1, 'curr')
        self.SetCurrent(0, chan2)
        # turn on
        self.SetOutput(1, chan1)
        self.SetOutput(1, chan2)
        time.sleep(1)
        # perform IV sweep
        v1 = []
        i1 = []
        v2 = []
        for i in i_arr:
            self.SetCurrent(i, chan1)
            v1.append(self.GetVoltage(chan1))
            v2.append(self.GetVoltage(chan2))
            i1.append(self.GetCurrent(chan1))

        # turn off
        self.SetOutput(0, chan1)
        self.SetOutput(0, chan2)

        if visualize:
            fig, ax1 = plt.subplots()
            ax1.plot(i1, v1, label='CH1', color='blue')
            ax1.set_ylabel('Voltage CH1 (V)', color='blue')
            ax1.set_xlabel('Current CH1 (A)', color='blue')

            ax2 = ax1.twinx()
            ax2.plot(i1, v2, label='CH2', color='red')
            ax2.set_ylabel('Voltage CH2 (V)', color='red')
            ax2.set_xlabel('Current CH1 (A)', color='red')

            ax2.set_xlim(ax1.get_xlim())
            ax2.set_ylim(ax1.get_ylim())
            
            ax1.set_title(f'sweep_2CH_IV. CH1= {chan1} - CH2 = {chan2}')
            fig.show()
        return v1, i1, v2
    
    def SweepVV_independent(self, ch1='A', ch2='B', v1_start=0, v1_stop=5, v2_bias=0, pts=100, visualize=True):
        import numpy as np
        import matplotlib.pyplot as plt
        self.reset()
        self.SetOutputMode(ch1, 'volt')
        self.SetOutputMode(ch2, 'volt')
    
        v_arr = np.linspace(v1_start, v1_stop, pts)
        self.SetVoltage(0, ch1)
        self.SetVoltage(v2_bias, ch2)
    
        i1 = []
        v1 = []
        i2 = []
        v2 = []
    
        self.SetOutput(1, ch1)
        self.SetOutput(1, ch2)
    
        for v in v_arr:
            self.SetVoltage(v, ch1)
            v1.append(self.GetVoltage(ch1))
            i1.append(self.GetCurrent(ch1))
            v2.append(self.GetVoltage(ch2))
            i2.append(self.GetCurrent(ch2))
    
        # turn off
        self.SetOutput(0, ch1)
        self.SetOutput(0, ch2)
    
        if visualize:
            fig1, ax1 = plt.subplots()
            ax1.plot(v1, i1, label='CH1 (PS)', color='blue')
            ax1.set_xlabel('Voltage CH1 (V)', color='blue')
            ax1.set_ylabel('Current CH1 (A)', color='blue')
            ax1.set_title(f'sweep_2CH_independent. CH1')
            fig1.show()
    
            fig2, ax2 = plt.subplots()
            ax2.plot(v2, i2, label='CH2 (PD)', color='red')
            ax2.set_xlabel('Voltage CH2 (V)', color='red')
            ax2.set_ylabel('Current CH1 (A)', color='red')
            ax1.set_title(f'sweep_2CH_independent. CH2')
            fig2.show()
        return v1, i1, v2, i2

    def SweepVI_independent(self, ch1='A', ch2='B', v1_start=0, v1_stop=5, curr2=0, pts=100, visualize=True):
        import numpy as np
        import matplotlib.pyplot as plt
        self.reset()
        self.SetOutputMode(ch1, 'volt')
        self.SetOutputMode(ch2, 'curr')
    
        v_arr = np.linspace(v1_start, v1_stop, pts)
        self.SetVoltage(0, ch1)
        self.SetCurrent(curr2, ch2)
    
        i1 = []
        v1 = []
        i2 = []
        v2 = []
    
        self.SetOutput(1, ch1)
        self.SetOutput(1, ch2)
    
        for v in v_arr:
            self.SetVoltage(v, ch1)
            v1.append(self.GetVoltage(ch1))
            i1.append(self.GetCurrent(ch1))
            v2.append(self.GetVoltage(ch2))
            i2.append(self.GetCurrent(ch2))
    
        # turn off
        self.SetOutput(0, ch1)
        self.SetOutput(0, ch2)
    
        if visualize:
            fig1, ax1 = plt.subplots()
            ax1.plot(v1, i1, label='CH1', color='blue')
            ax1.set_xlabel('Voltage CH1 (V)', color='blue')
            ax1.set_ylabel('Current CH1 (A)', color='blue')
            ax1.set_title(f'sweep_2CH_independent. CH1')
            fig1.show()
    
            fig2, ax2 = plt.subplots()
            ax2.plot(v2, i2, label='CH2', color='red')
            ax2.set_xlabel('Voltage CH2 (V)', color='red')
            ax2.set_ylabel('Current CH2 (A)', color='red')
            ax1.set_title(f'sweep_2CH_independent. CH2')
            fig2.show()

        return v1, i1, v2, i2