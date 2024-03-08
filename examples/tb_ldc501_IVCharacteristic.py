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



#if True:
#    ldc_gpib = 'visa://192.168.137.1/GPIB0::2::INSTR'
#    pm_gpib  = 'visa://192.168.137.1/GPIB0::20::INSTR'
#else:
#    ldc_gpib = 'visa://10.2.137.163/GPIB0::2::INSTR'
#    pm_gpib = 'visa://10.2.137.163/GPIB0::20::INSTR'

if True:
    ldc_gpib = 'GPIB0::2::INSTR'
    pm_gpib  = 'GPIB0::19::INSTR'
else:
    ldc_gpib = 'visa://10.2.137.163/GPIB0::2::INSTR'
    pm_gpib = 'visa://10.2.137.163/GPIB0::20::INSTR'



ldc = ldc_srs_ldc500(rm.open_resource(ldc_gpib), chan='')
pm = PowerMonitor_keysight(rm.open_resource(pm_gpib), chan='1', slot=1)

# %% sequence definition
sequence = SetupLDC501(ldc, pm)

sequence.verbose = True
sequence.visual = True
sequence.saveplot = True
sequence.Imin = 0   #mA
sequence.Imax = 90 #mA
sequence.numPts = 90 + 1
sequence.temperature = 25 # Degrees C


 # Power Monitor Settings:
sequence.pm.SetWavl(1550)
sequence.pm.SetPwrUnit('mW')
sequence.pm.SetAutoRanging(1)
sequence.pm.SetPwrRange(0)


 
chipID = 'DPLAB_ARL_AR_CL30'
measID = '25LIV_CL30_25dB_att_'
date = datetime.now().strftime("%Y-%m-%d_%H-%M_")
basedir = 'C:\\!Data/'
#basedir = '/Volumes/Shared/QMI/CartSoftware/SiEPICLab/siepiclab/'
datadir = basedir + chipID


sequence.file_name = str(datadir)+ '/'+ str(date) + str(measID) +f'_{sequence.temperature}degC_{sequence.Imin}-{sequence.Imax}mA'

#sequence.ldc.tecON()
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
df.to_csv(sequence.file_name +".csv", sep=',',index=False)
