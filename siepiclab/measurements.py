# -*- coding: utf-8 -*-
"""
SiEPIClab measurements module.

Mustafa Hammood, SiEPIC Kits, 2022
"""

class lab_setup:
    """Experiment lab setup abstraction class."""

    def __init__(self, instruments):
        self.instruments = instruments
        self.settings = self.GetSettings()

    def GetSettings(self):
        """
        Get the settings of all the instruments in the experiment setup.

        Returns
        -------
        settings : list
            list of instrument states.

        """
        settings = []
        for instr in self.instruments:
            settings.append(instr.GetState())
        return settings

    def SetSettings(self, settings):
        """
        Set the settings of all the instruments in the experiment setup.

        Parameters
        ----------
        settings : list
            list of instrument states.

        Returns
        -------
        None

        """
        for idx, inst in enumerate(self.instruments):
            inst.SetState(self.settings[idx].state)


class routine:
    """Operations sequence abstraction class."""

    def __init__(self):
        return

    def execute(self):
        """Execute the routine."""
        settings = self.experiment.GetSettings()  # get the initial state of the experiment

        try:
            self.sequence()
        except AttributeError:
            print('ERR: No sequence is defined in this routine.')
            return

        # reset the experiment state to the initial state
        self.experiment.SetSettings(settings)


class OptimizePolarization(routine):
    """
    Routine to optimize the received polarization state.

    Setup:
        laser -SMF28-> polCtrl -SMF28-> powerMonitor

    Sweep the polarization state of the polarization controller, record the optical power
    received from the laser to the optical power monitor.

    Parameters
    ----------
    PolCtrl : SiEPIClab instrument type
        Optical Polarization controller instrument instance.
    pm : SiEPIClab instrument type
        Optical power monitor instrument instance.
    laser : SiEPIClab instrument type
        Optical laser instrument instance.
    time : int, optional
        Scan time (seconds). The longer the more accurate the scan.
        The default is 15 seconds.
    verbose : Boolean, optional
        Flag to trigger verbose mode for debugging. The default is False.

    Returns
    -------
    None.

    """

    def __init__(self, polCtrl, powerMonitor, laser, scantime=15, verbose=False):
        self.polCtrl = polCtrl
        self.powerMonitor = powerMonitor
        self.laser = laser
        self.scantime = scantime
        self.verbose = verbose

        instruments = [polCtrl, powerMonitor, laser]
        self.experiment = lab_setup(instruments)
