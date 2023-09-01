# -*- coding: utf-8 -*-

"""
SiEPIClab sequence application example.

Sequence to perform OSA Sweep
Test setup:
    #Filout

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

if False:
    ldc_gpib = 'GPIB0::2::INSTR'
    pm_gpib  = 'GPIB0::20::INSTR'
else:
    osa_gpib = 'visa://192.168.137.1/GPIB0::1::INSTR'
    ldc_gpib = 'visa://192.168.137.1/GPIB0::2::INSTR'


osa = osa_agilent(rm.open_resource(osa_gpib), chan='')
ldc = ldc_srs_ldc500(rm.open_resource(ldc_gpib), chan='')


print(osa.identify())
print(ldc.identify())


# %%

ldc.LDON()
ldc.SetLDcurrent(20)
# %%
osa.SingleSweep()

# %%
osa.SetWavlCenter(1270)
print(osa.WavlCenter())

osa.SetWavlSpan(1)
print(osa.WavlSpan())

numpts = osa.getTracePoints()

print(numpts)
# %%
import matplotlib.pyplot as plt


biases = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

wavl = []
pwr = []

osa.SetWavlSpan(3)

ldc.LDON()
ldc.SetLDcurrent(0)


for bias in biases:
    
    # Biases the Laser
    ldc.SetLDcurrent(bias)
    
    # Does a sweep
    osa.SingleSweep()
    
    # Gets the trace data
    wl, p = osa.getTrace()
    
    # Adds it to a list
    wavl.append(wl)
    pwr.append(p)

for i in range(0, len(biases)):
    plt.plot(wavl[i], pwr[i])




# %%
type(pwr)
# %%
