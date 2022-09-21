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

from datetime import datetime
from siepiclab.sequences.SetupLDC501 import SetupLDC501
from siepiclab.drivers.ldc_srs_ldc500 import ldc_srs_ldc500
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
rm = visa.ResourceManager()



if True:
    ldc_gpib = 'GPIB0::2::INSTR'
    pm_gpib  = 'GPIB0::20::INSTR'
else:
    ldc_gpib = 'visa://10.2.137.163/GPIB0::2::INSTR'
    pm_gpib = 'visa://10.2.137.163/GPIB0::20::INSTR'


ldc = ldc_srs_ldc500(rm.open_resource(ldc_gpib), chan='')
pm = PowerMonitor_keysight(rm.open_resource(pm_gpib), chan='1', slot=2)

# %% sequence definition
sequence = SetupLDC501(ldc, pm)

sequence.verbose = True
sequence.visual = True
sequence.saveplot = True
sequence.numPts = 35
sequence.Imin = 1
sequence.Imax = 35

sequence.temperature = 20


chipID = 'SHUKSAN-A4'
date = datetime.now().strftime("%y-%m-%d_")
basedir = 'C:/Users/testStation/Desktop/Data/'
datadir = basedir + date + chipID


sequence.file_name = str(datadir)+ '/'+ str(date) + str(chipID) +f'_{sequence.temperature}degC_{sequence.Imin}-{sequence.Imax}A-sweep'

# %% 
sequence.execute()

# Save as a .pkl file:
sequence.results.save(sequence.file_name)

# Save as CSV Data:
data1 = sequence.results.data['currents']
data2 = sequence.results.data['voltages']
data3 = sequence.results.data['powers']
data4 = sequence.results.data['powersdbm']

df = pd.DataFrame({"currents": data1, 'voltages':data2, 'powers':data3, 'powersdbm':data4})
df.to_csv(sequence.file_name, sep=',',index=False)

pass


# %%
