"""
SiEPIClab measurement routine.

Testbench for the 11896A polarization controller class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
from siepiclab import measurements


class testbench_PowerMonitor_keysight(measurements.sequence):
    """Testbench measurement routine for the Power Monitor class."""

    def __init__(self, pm):
        self.pm = pm

        instruments = [pm]
        self.experiment = measurements.lab_setup(instruments)

    def instructions(self):
        """Sequence of the routine."""
        import time
        print('Paddle position reading: ' + str(self.polCtrl.GetPaddlePosition()))
        print('All Paddles position reading: ' + str(self.polCtrl.GetPaddlePositionAll()))
        print('Scan rate reading: ' + str(self.polCtrl.GetScanRate()))

        print('Setting paddle position to: '+str(self.paddlePosition))
        result = self.polCtrl.SetPaddlePosition(1, self.paddlePosition, confirm=True)
        print('Reading paddle position at: '+str(result))

        print('Setting all paddle position to: '+str(self.paddlePositionAll))
        result = self.polCtrl.SetPaddlePositionAll(self.paddlePositionAll, confirm=True)
        print('Reading all paddle position at: '+str(result))

        print('Setting scan rate to: '+str(self.scanrate))
        result = self.polCtrl.SetScanRate(self.scanrate, confirm=True)
        print('Reading scan rate to: '+str(result))

        self.polCtrl.StartScan()
        self.polCtrl.StopScan()
        time.sleep(5)
        print("Testbench ran successfully.")
