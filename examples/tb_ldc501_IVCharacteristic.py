# -*- coding: utf-8 -*-

"""
SiEPIClab sequence application example.

Sequence to perform IV Characterization of Laser.
Test setup:
    LDC501 -BNC-> || DUT || -SMF-> Power Monitor

Davin Birdi, 2022
With Templates and support from Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pandas as pd
import pyvisa as visa
from siepiclab.sequences.SetupLDC501 import SetupLDC501
from siepiclab.drivers.ldc_srs_ldc500 import ldc_srs_ldc500
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
rm = visa.ResourceManager()


# %% instruments definition
#print(rm.list_resources())

ldc_gpib = 'GPIB0::2::INSTR'
pm_gpib  = 'GPIB0::20::INSTR'

ldc = ldc_srs_ldc500(rm.open_resource(ldc_gpib), chan='')
pm = PowerMonitor_keysight(rm.open_resource(pm_gpib), chan='1')

# %% sequence definition
sequence = SetupLDC501(ldc, pm)

sequence.visual = True
sequence.saveplot = True
sequence.numPts = 36
sequence.Imin = 0
sequence.Imax = 35

datadir = 'testLD'
sequence.file_name = str(datadir)+'/2022-08-23_0-35mA-2'

sequence.execute()

# Save as a .pkl file:
sequence.results.save(sequence.file_name)

# Save as CSV Data:
data1 = sequence['currents']
data2 = sequence['voltages']
data3 = sequence['powers']



pass


# %%
