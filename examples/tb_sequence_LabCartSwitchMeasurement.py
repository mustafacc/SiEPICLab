"""
SiEPIClab testbench.

Basic Testbench toggling through switch outputs.

Davin Birdi, UBC Photonics

With Credit to:
Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa

from siepiclab.drivers.opticalSwitch_jds import opticalSwitch_jds
from siepiclab.drivers.PolCtrl_keysight import PolCtrl_keysight
from siepiclab.drivers.tls_keysight import tls_keysight
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
from siepiclab.drivers.lwmm_keysight import lwmm_keysight

from siepiclab.sequences.SwitchSequences import SwitchSequences


import numpy as np
from matplotlib import pyplot as plt
from pandas import DataFrame
from datetime import datetime


rm = visa.ResourceManager()

#print(rm.list_resources())
# %% instruments definition

if True:
    switch_gpib = 'GPIB0::7::INSTR'
    mf_gpib = 'GPIB0::20::INSTR'
    pol_gpib = 'GPIB0::8::INSTR'
else:
    switch_gpib = 'visa://10.2.137.163/GPIB0::7::INSTR'
    mf_gpib = 'visa://10.2.137.163/GPIB0::20::INSTR'
    pol_gpib = 'visa://10.2.137.163/GPIB0::8::INSTR'


jds = opticalSwitch_jds(rm.open_resource(switch_gpib), chan='')
tls = tls_keysight(rm.open_resource(mf_gpib), chan='2')
pol = PolCtrl_keysight(rm.open_resource(pol_gpib), chan='')
pm = PowerMonitor_keysight(rm.open_resource(mf_gpib), chan='1', slot=1)
mf = lwmm_keysight(rm.open_resource(mf_gpib))


# %% Chip MetaData:
#chipID = 'MTPLoopback'
chipID = 'AEPONYX_W5-C3L6-F'
user = 'dbirdi'
note = ''

date = datetime.now().strftime("%Y-%m-%d")
basedir = '././TestData/AEPONYX/' + date + '_' + user + '/'
#basedir = '././TestData/' + date + user + '/'
datadir = basedir + chipID

file_name = str(datadir)+ '/'+ str(date) + str(chipID)

sequence = SwitchSequences(tls, pm, pol, mf, jds, verbose=True, saveplot=True, visual=True)
sequence.range = [4,5,7]
sequence.seq_polopt.scantime = 45
sequence.WLSweep = True 
sequence.file_name = file_name
sequence.results.add('chipID', chipID)
sequence.results.add('user', user)
sequence.results.add('date', date)
sequence.results.add('note', note)

sequence.WLSweep = True

sequence.devlist = {
    'dev2-3': 4,
    'dev4-5': 5,
    'dev7-12': 7
}

# %% Experiment Calibration
Calibration = False
if Calibration:
    calibration = sequence
    calibration.file_name = file_name + '_Calibration'

    # Begin the Calibration & Measurement:
    while input('Press Y to start Calibration: ').lower() != 'y':
        pass
    calibration.execute()
    calibration.results.save(calibration.file_name)


# %% Experiment Measurement
sequence.file_name = file_name
while input('Press Y to start Measurement: ').lower() != 'y':
    pass
sequence.execute()
sequence.results.save(sequence.file_name)

pass
