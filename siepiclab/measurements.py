# -*- coding: utf-8 -*-
"""
SiEPIClab measurements module.

Mustafa Hammood, SiEPIC Kits, 2022
"""
import pickle
from datetime import datetime


class routine:
    """Measurement routine abstraction class."""

    def __init__(self):
        self.routine = dict()
        return

    def add(self, name, sequence):
        """Add a sequence to the routine."""
        self.routine[str(name)] = sequence


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
        for idx, instr in enumerate(self.instruments):
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


class results:
    """Measurement results abstraction class."""

    def __init__(self):
        self.data = dict()
        return

    def add(self, name, data):
        """
        Add dataset to the results.

        Example
        ----------
            voltage = [1,2,3]
            current = [1,2,3]
            results = siepiclab.measurements.results()
            results.add('voltage', voltage)
            results.add('current', current)

        Parameters
        ----------
        name : string
            Name of the data to add.
        data : Any
            Content of the data.

        Returns
        -------
        None.

        """
        self.data[str(name)] = data

    def save(self, file_name=None, timestamp=False):
        """
        Export the results to a pickle file (.pkl).

        Parameters
        ----------
        file_name : string, optional
            File name and directory of the file to save. The default is None.
                Current timestamp will be used if filename is None.
        timestamp : Boolean, optional
            Flag to add a timestamp in the format of YYYYMMDDHHMMSS format.

        Returns
        -------
        None.

        """
        if timestamp or file_name is None:
            if file_name is None:
                file_name = str(datetime.now().strftime('%Y%m%d%H%M%S'))
            else:
                file_name = str(datetime.now().strftime('%Y%m%d%H%M%S'))+'_'+file_name

        with open(str(file_name)+'.pkl', 'wb') as f:
            pickle.dump(self.data, f)

    def load(self, file_name):
        """
        Import previousily exported results pickle file (.pkl).

        Parameters
        ----------
        file_name : string, optional
            File name and directory of the file to save.

        Returns
        -------
        Dictionary
            Dictionary containing the loaded data results.

        """
        with open(str(file_name)+'.pkl', 'rb') as f:
            return pickle.load(f)


class sequence:
    """Operations sequence abstraction class."""

    def __init__(self, visual=False, verbose=False, saveplot=False):
        self.verbose = verbose
        self.visual = visual
        self.saveplot = saveplot
        self.results = results()
        self.instruments = []
        self.file_name = ''
        return

    def execute(self):
        """Execute the sequence."""
        # get the initial state of the experiment
        settings = self.experiment.GetSettings(self.verbose)

        # add the instrument state to the results file
        self.results.add('instruments', [instr.identify() for instr in self.instruments])
        for idx, state in enumerate(settings):
            self.results.data['state_'+self.instruments[idx].identify()
                              ] = str(state.GetState())

        self.instructions()

        # reset the experiment state to the initial state
        self.experiment.SetSettings(settings)
