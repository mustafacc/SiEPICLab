# -*- coding: utf-8 -*-
"""
SiEPIClab measurements module.

Mustafa Hammood, SiEPIC Kits, 2022
"""


class lab_setup:
    """Experiment lab setup abstraction class."""

    def __init__(self, instruments, verbose=False):
        self.instruments = instruments
        self.settings = self.GetSettings()
        self.verbose = verbose

    def GetSettings(self, verbose=False):
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
            if verbose:
                print('State of: ' + instr.identify())
                print(str(instr.GetState().state)+'\n')
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


class sequence:
    """Operations sequence abstraction class."""

    def __init__(self, visual=False, verbose=False):
        self.verbose = verbose
        self.visual = visual
        return

    def execute(self):
        """Execute the routine."""
        # get the initial state of the experiment
        settings = self.experiment.GetSettings(self.verbose)

        self.instructions()

        # reset the experiment state to the initial state
        self.experiment.SetSettings(settings)
