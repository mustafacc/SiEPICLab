"""
SiEPIClab instrument driver.

Instrument driver for the Stanford Instrument SRS LDC500 Series.
Laser Diode Controller.

Mustafa Hammood, SiEPIC Kits, 2022
Thank you Hossam Shoman.
"""

from siepiclab import instruments
import time


class ldc_srs_ldc500(instruments.instr_VISA):
    """
    Stanford Instrument SRS LDC500 Series Controller class.

    Includes:
        SRS LDC501
    """

    def GetState(self):
        """Return an instance of the instrument."""
        currState = instruments.state()
        return currState

    def SetState(self, state):

        return 0

    # TEC Settings:
    def GetTemperature(self):
        """
        Get the temperature of the DUT.

        Returns
        -------
        float
            The measured temperature in Celsius.

        """
        return float(self.addr.query('TTRD?'))

    def SetTemperature(self, temp, verbose=False, wait=False):
        """
        Set the temperature of the DUT.

        Parameters
        ----------
        temp : float
            The temperature to set (in Celsius).
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        self.addr.write('TEMP %g' % float(temp))
        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetTemperature())

    def tecON(self):
        self.addr.write('TEON ON')

    def tecOFF(self):
        self.addr.write('TEON OFF')

    def tecMode(self, mode):
        self.tecOFF()
        if mode == 'CC':
            self.addr.write('TMOD 0') # Set mode to CC
        elif mode == 'CT':
            self.addr.write('TMOD 1') # Set mode to CT
        else:
            raise NameError('Input only CC or CT.')

    # LD Settings:
    def LDON(self):  # turn current on
        self.addr.write('SILD 0')  # set current to 0 first
        self.addr.write('LDON ON')

    def LDOFF(self):  # turn current on
        self.addr.write('SILD 0')  # set current to 0 first
        time.sleep(1)
        self.addr.write('LDON OFF')

    def GetLDSTATUS(self):
        re = self.addr.query('LDON?')
        if float(re) == 1:
            print('LD is ON.')
            return True
        elif float(re) == 0:
            print('LD is OFF.')
            return False

    def GetLDVlim(self):
        return(float(self.addr.query('SVLM?')))

    def SetLDVlim(self, Vlim, verbose=False, wait=False):
        """
        Set voltage limit for the laser diode.

        Parameters
        ----------
        Vlim : float
            Voltage limit (volts).
        verbose : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        self.addr.write('SVLM %g' % Vlim)
        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetLDVlim())

    def GetLDIlim(self):
        return(float(self.addr.query('SILM?')))

    def SetLDIlim(self, Ilim, verbose=False, wait=False):
        self.addr.write('SILM %g' % Ilim)
        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetLDIlim())

    def GetLDcurrent(self):  # read current in mA
        res = self.addr.query('RILD?')
        return(float(res))

    def SetLDcurrent(self, Iset, verbose=False, wait=False):  # current setpoint in mA
        self.addr.write('SILD %g' % Iset)
        if wait or verbose:
            self.wait()
        if verbose:
            return(self.GetLDcurrent())

    def GetLDvoltage(self):  # read voltage
        res = self.addr.query('RVLD?')
        return(float(res))

    # laser configuration
    def SetLDIrange(self, toggle):  # range
        if toggle == 1:
            self.addr.write('RNGE HIGH')
        elif toggle == 0:
            self.addr.write('RNGE LOW')
        else:
            print("ERR: Invalid setting. Options are 1: HIGH, 0: LOW.")

    # PD Settings:
    def GetPDbias(self):
        return(float(self.addr.query('BIAS?')))

    def SetPDbias(self, Vbias):
        self.addr.write('BIAS %g' % float(Vbias))

    def GetPDcurrentLim(self):
        return(float(self.addr.query('PILM?')))

    def GetPDpowerLim(self):
        return(float(self.addr.query('PWLM?')))

    def GetPDcurrent(self):
        return(float(self.addr.query('RIPD?')))

    def GetPDpower(self):
        return(float(self.addr.query('RWPD?')))

    def GetPDresp(self):
        return(float(self.addr.query('RESP?')))
