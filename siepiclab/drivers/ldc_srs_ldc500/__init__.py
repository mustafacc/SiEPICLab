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

    def GetTemperature(self):
        """
        Get the temperature of the DUT.

        Returns
        -------
        float
            The measured temperature in Celsius.

        """
        return float(self.instrument.query('TTRD?'))

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

    def getLDVlimit(self):
        return(float(self.instrument.query('SVLM?')))

    def setLDVlimit(self, Vlim):  # set voltage limit
        self.addr.write('SVLM %g' % Vlim)

    def GetLDIlimit(self):
        return(float(self.instrument.query('SILM?')))

    def SetLDIlimit(self, Ilim):
        self.addr.write('SILM %g' % Ilim)

    def LDON(self):  # turn current on
        self.addr.write('SILD 0')  # set current to 0 first
        self.addr.write('LDON ON')

    def LDOFF(self):  # turn current on
        self.addr.write('SILD 0')  # set current to 0 first
        time.sleep(1)
        self.addr.write('LDON OFF')

    def getLDturnSTATUS(self):
        res = self.addr.query('LDON?')
        if float(res) == 1:
            print('LD is ON')
            return 1
        elif float(res) == 0:
            print('LD is OFF')
            return 0

    def setLDcurrent(self, Iset):  # current setpoint in mA
        self.addr.write('SILD %g' % Iset)

    # laser monitor
    def getLDcurrent(self):  # read current in mA
        res = self.addr.query('RILD?')
        return(float(res))
#        print('LD current: %g'%float(res))

    def getLDvoltage(self):  # read voltage
        res = self.addr.query('RVLD?')
        return(float(res))
#        print('LD voltage: %g'%float(res))

    # laser configuration
    def setLDIrange(self, toggle):  # range
        if toggle == 1:
            self.addr.write('RNGE HIGH')
        elif toggle == 0:
            self.addr.write('RNGE LOW')
        else:
            print("the range should either be 1 or 0 for high or low")

    def getPDcurrentLimit(self):
        return(float(self.instrument.query('PILM?')))

    def getPDpowerLimit(self):
        return(float(self.instrument.query('PWLM?')))

    def getPDcurrent(self):
        return(float(self.instrument.query('RIPD?')))

    def getPDpower(self):
        return(float(self.instrument.query('RWPD?')))

    def getPDresp(self):
        return(float(self.instrument.query('RESP?')))

    def getPDbias(self):
        return(float(self.instrument.query('BIAS?')))

    def setPDbias(self, Vbias):
        self.addr.write('BIAS %g' % float(Vbias))
