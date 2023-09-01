# -*- coding: utf-8 -*-

"""
SiEPIClab sequence application example.

Sequence to perform OSA Sweep
Test setup:
    LDC501 -BNC-> || DUT || -SMF-> Power Monitor

Davin Birdi, 2023
@With Templates and support from Mustafa Hammood, SiEPIC Kits, 2022
@Based on original work by Hossam Shossam
"""
# %%
import pandas as pd
import pyvisa as visa

from datetime import datetime
from siepiclab.sequences.SetupLDC501 import SetupLDC501
from siepiclab.drivers.ldc_srs_ldc500 import ldc_srs_ldc500
from siepiclab.drivers.osa_agilent import osa_agilent
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
rm = visa.ResourceManager()


# %%
if False:
    ldc_gpib = 'GPIB0::2::INSTR'
    pm_gpib  = 'GPIB0::20::INSTR'
else:
    osa_gpib = 'visa://192.168.137.1/GPIB0::1::INSTR'
    ldc_gpib = 'visa://192.168.137.1/GPIB0::2::INSTR'
    #pm_gpib = 'visa://10.2.137.163/GPIB0::20::INSTR'


osa = osa_agilent(rm.open_resource(osa_gpib), chan='')
ldc = ldc_srs_ldc500(rm.open_resource(ldc_gpib), chan='')
#pm = PowerMonitor_keysight(rm.open_resource(pm_gpib), chan='1', slot=2)

# %%

print(osa.identify())
print(ldc.identify())

# %%

print("Getting A trace")

numpoints = 101


osa.



# %%
