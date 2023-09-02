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
import numpy as np
import pyvisa as visa
import matplotlib.pyplot as plt

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
def simple_test():
    ldc.LDON()
    ldc.SetLDcurrent(20)

    osa.SingleSweep()

    osa.SetWavlCenter(1270)
    print(osa.WavlCenter())

    osa.SetWavlSpan(1)
    print(osa.WavlSpan())

    numpts = osa.getTracePoints()
    print(numpts)
    osa.SingleSweep()
    wavl, pwr = osa.getTrace()
    plt.plot(wavl, pwr)

    # Notice the plot plots before results are shown.

simple_test()
# %% LDC Current Bias Scan
ldc.GetTemperature()
ldc.SetTemperature(25)
ldc.tecON()



biases = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])

wavl = []
pwr = []

data = pd.DataFrame()

osa.SetWavlSpan(1)

ldc.LDON()
ldc.SetLDcurrent(0)


for bias in biases:
    
    # Biases the Laser
    ldc.SetLDcurrent(bias)
    
    # Does a sweep
    osa.SingleSweep()
    
    # Gets the trace data
    wl, p = osa.getTrace()
    
    # Adds Power Data
    data[f'{bias:0.2f}'] = p

# Get the Wavelength Once
data['wavl'] = wl
date = data.set_index('wavl')

## Turn off.
ldc.SetLDcurrent(0)
ldc.LDOFF()
ldc.tecOFF()

# %% Plot and Save to CSV

plt.plot(data)
dirname = '/Volumes/Shared/QMI/CartSoftware/'
date = datetime.now().strftime("%Y-%m-%d")
filename = 'osa_currentsweep.csv'

savename = dirname + date + filename

data.to_csv(savename)


# %% Verify Reading the same File:
df = pd.read_csv('/Volumes/Shared/QMI/CartSoftware/2023-09-01osa_currentsweep.csv', index_col='wavl')
df
# %%
