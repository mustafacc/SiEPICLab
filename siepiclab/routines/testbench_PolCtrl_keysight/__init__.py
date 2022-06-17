"""
SiEPIClab measurement routine.

Testbench for the 11896A polarization controller class.

Mustafa Hammood, SiEPIC Kits, 2022
"""

from siepiclab import measurements
class testbench(measurements.routine):
    """Testbench sequence."""

    def __init__(self, polCtrl, paddlePosition):
        self.polCtrl = polCtrl
        self.paddlePosition = paddlePosition

        instruments = [polCtrl]
        self.experiment = measurements.lab_setup(instruments)

    def sequence(self):
        """Sequence of the routine."""
        import time
        self.polCtrl.SetPaddlePosition(1, self.paddlePosition)
        time.sleep(5)