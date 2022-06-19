"""
SiEPIClab instrument driver.

Instrument driver for the HP-Agilent-Keysight polarization controller instruments.

Mustafa Hammood, SiEPIC Kits, 2022
"""

from siepiclab import instruments


class PolCtrl_keysight(instruments.instr_VISA):
    """
    HP-Agilent-Keysight Polarization Controller class.

    Includes:
        11896A
    """

    def GetState(self):
        """Return an instance of the instrument."""
        currState = instruments.state()
        currState.AddState('PaddlePositionAll', self.GetPaddlePositionAll())
        currState.AddState('ScanRate', self.GetScanRate())
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
        self.SetPaddlePositionAll(state['PaddlePositionAll'], confirm=True)
        self.SetScanRate(state['ScanRate'], confirm=True)

    def StartScan(self):
        """Start a random polarization scan."""
        self.addr.write('INIT:IMM')

    def StopScan(self, wait=False):
        """Stop a random polarization scan."""
        self.addr.write('ABOR')
        if wait:
            self.wait()

    def GetScanRate(self):
        """
        Get the polarization scan rate of the instrument.

        Returns
        -------
        scanrate : int
            Scan rate from the instrument. 1 is the slowest, 8 is the fastest.

        """
        re = self.addr.query('SCAN:RATE?')
        scanrate = int(str(re.strip()))
        return scanrate

    def SetScanRate(self, scanrate, confirm=False, wait=False):
        """
        Set the polarization scan rate of the instrument.

        Parameters
        ----------
        scanrate : int
            Scan rate from the instrument. 1 is the slowest, 8 is the fastest.

        Returns
        -------
        None.

        """
        self.addr.write('SCAN:RATE '+str(int(scanrate)))
        if wait or confirm:
            self.wait()
        if confirm:
            return(self.GetScanRate())

    def GetPaddlePosition(self, paddle=1):
        """
        Get the position of one paddle in the instrument (of the 3).

        Parameters
        ----------
        paddle : int, optional
            Paddle ID in the instrument. 1,2, and 3 are valid. The default is 1.

        Returns
        -------
        position : int
            Paddle position (value from 0 to 999).

        """
        re = self.addr.query('PADD'+str(int(paddle))+':POS?')
        position = int(str(re.strip()))
        return position

    def SetPaddlePosition(self, paddle=1, position=500, confirm=False, wait=False):
        """
        Set the position of an given paddle in the instrument.

        Parameters
        ----------
        paddle : int, optional
            Paddle ID in the instrument. 1,2, and 3 are valid. The default is 1.
        position : int
            Paddle position (value from 0 to 999).
        confirm : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        self.addr.write('PADD'+str(int(paddle)) + ':POS '+str(int(position)))
        if wait or confirm:
            self.wait()
        if confirm:
            return(self.GetPaddlePosition(paddle))

    def GetPaddlePositionAll(self, numPaddles=4):
        """
        Get all the paddles position in the instrument.

        Parameters
        ----------
        numPaddles : TYPE, optional
            DESCRIPTION. The default is 4.

        Returns
        -------
        paddlePositions : list
            list of ints of each paddle position (each is from 0 to 999).

        """
        paddlePositions = []
        for pad in range(numPaddles):
            paddlePositions.append(self.GetPaddlePosition(pad+1))
        return paddlePositions

    def SetPaddlePositionAll(self, positions=[500, 500, 500, 500], confirm=False, wait=False):
        """
        Set the paddle positions for all paddles in the instruemnt.

        Parameters
        ----------
        positions : [list], optional
            List of ints of the paddles positions. The default is [500, 500, 500, 500].
        confirm : Boolean, optional
            Return the instrument reading after the operation.
            The default is False.
        wait : Boolean, optional
            Block program until the query is done. The default is False.

        Returns
        -------
        None.

        """
        for paddle in range(len(positions)):
            self.SetPaddlePosition(paddle+1, positions[paddle])
        if wait or confirm:
            self.wait()
        if confirm:
            return(self.GetPaddlePositionAll())
