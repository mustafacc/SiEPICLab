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


class sequence:
    """Operations sequence abstraction class."""

    def __init__(self):
        return

    def execute(self):
        """Execute the routine."""
        settings = self.experiment.GetSettings()  # get the initial state of the experiment

        try:
            self.instructions()
        except AttributeError:
            print('ERR: No sequence is defined in this routine.')
            return

        # reset the experiment state to the initial state
        self.experiment.SetSettings(settings)
