# -*- coding: utf-8 -*-

"""
SiEPIClab sequence application example.

Sequence to perform OSA Sweep
Test setup:
    TLS@1540nm  --> PolPaddles --> (SOA DUT) --> OSA
    LDC Electrical Probes --> (SOA DUT)

Steps:
    Run this script with TLS set to [-10, -5, 0, 5] dBm and update the name saved.
    Each iteration records the OSA Spectrum to measure gain while at a specified Electrical Bias

Reference Measurement:
    SOA Amplified Spontaneous Emission (ASE) at each TLS setting (0mA Bias current)
    Gain is calculated as Power@1540nm minus ASE@1540nm 

    

OSA Settings:
    Start: 1460nm 
    Stop: 1610nm
    Sensitivity: -80dB
    Repeat Sweep: OFF
    Resolution BW: 0.06nm

TLS Settings:
    Wavelength: 1540nm

Polarization Optimization:
    TLS: -10dbM
    OSA Start Stop: 1539.5-1540.5nm
    Continuous Mode
    Resolution: 0.1nm
    Marker On (Able to see peak location & strength)

    



Davin Birdi and Josh Gibbs, 2024
@With Templates and support from Mustafa Hammood, SiEPIC Kits, 2022
@Based on original work by Hossam Shossam
"""
# %%
import pandas as pd
import numpy as np
import pyvisa as visa
import matplotlib.pyplot as plt
from time import sleep

from datetime import datetime
from siepiclab.sequences.SetupLDC501 import SetupLDC501
from siepiclab.drivers.ldc_srs_ldc500 import ldc_srs_ldc500
from siepiclab.drivers.osa_agilent import osa_agilent
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
rm = visa.ResourceManager()

if True:
    osa_gpib = 'GPIB0::1::INSTR'
    ldc_gpib = 'GPIB0::2::INSTR'
    #pm_gpib  = 'GPIB0::20::INSTR'
else:
    osa_gpib = 'visa://192.168.137.1/GPIB0::1::INSTR'
    ldc_gpib = 'visa://192.168.137.1/GPIB0::2::INSTR'


osa = osa_agilent(rm.open_resource(osa_gpib), chan='')
ldc = ldc_srs_ldc500(rm.open_resource(ldc_gpib), chan='')


print(osa.identify())
print(ldc.identify())

# %%
ldc.GetTemperature()
ldc.SetTemperature(25)
ldc.tecON()
ldc.LDON()
ldc.SetLDcurrent(2)

#osa.SetWavlCenter(1550)
#osa.SetWavlSpan(10)
temperatures = 25#np.array([20, 25, 30, 35, 40, 45])
biases = np.array([0, 25, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500])
wavl = []
pwr = []
data = pd.DataFrame()

print('Starting LDC Sweeps...')
for bias in biases:
    try:
        print(f'Setting Current to {bias}mA...')
        ldc.SetLDcurrent(bias)
        sleep(10)
        osa.SingleSweep()
        sleep(60)
        wavl, pwr = osa.getTrace()
        plt.plot(wavl, pwr)
        data[f'{bias:0.2f}'] = pwr
    except:
        input('Failed to connect to instrument, reconnecting...')

# ldc.SetLDcurrent(50)
# for temperature in temperatures:
#     try:
#         ldc.SetTemperature(temperature)
#         sleep(60)
#         osa.SingleSweep()
#         sleep(6)
#         wavl, pwr = osa.getTrace()
#         plt.plot(wavl, pwr)
#         data[f'{temperature:0.2f}'] = pwr
#     except:
#         input('Failed to connect to instrument, reconnecting...')




data['wavl'] = wavl
data = data.set_index('wavl')

## Turn off.
ldc.SetLDcurrent(0)
ldc.LDOFF()
#ldc.tecOFF()

# %% Plot and Save to CSV

plt.plot(data)


chipID = 'DPLAB_LightIC_SOA_V4'
measID = '-10dBm_PortA_1540nm_measPortB_OSA'
measID = '-10dBm_patch_cable'
date = datetime.now().strftime("%Y-%m-%d_%H-%M_")
basedir = 'C:\\!Data/'
datadir = basedir + chipID

savename = str(datadir) + "\\patch_cable\\" + str(date) + str(measID) 

data.to_csv(savename +".csv")



plt.show()


# %%
