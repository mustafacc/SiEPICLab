"""
SiEPIClab testbench.

Basic Testbench toggling through switch outputs.

Davin Birdi, UBC Photonics

With Credit to:
Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from measurements import sequence

from siepiclab.drivers.opticalSwitch_jds import opticalSwitch_jds
from siepiclab.drivers.PolCtrl_keysight import PolCtrl_keysight
from siepiclab.drivers.fls_keysight import fls_keysight
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight

from siepiclab.sequences.SwitchPath import SwitchPath
from siepiclab.sequences.SweepPolarization import SweepPolarization
from siepiclab.sequences.SweepPolarization_SwitchPaths import SweepPolarization_SwitchPaths


import numpy as np


rm = visa.ResourceManager()

print(rm.list_resources())
# %% instruments definition

if True:
    switch_gpib = 'GPIB0::7::INSTR'
    fls_gpib = 'GPIB0::20::INSTR'
    pol_gpib = 'GPIB0::8::INSTR'
else:
    switch_gpib = 'visa://10.2.137.163/GPIB0::7::INSTR'
    fls_gpib = 'visa://10.2.137.163/GPIB0::20::INSTR'
    pol_gpib = 'visa://10.2.137.163/GPIB0::8::INSTR'


jds = opticalSwitch_jds(rm.open_resource(switch_gpib), chan='')
fls = fls_keysight(rm.open_resource(fls_gpib), chan='2')
pol = PolCtrl_keysight(rm.open_resource(pol_gpib), chan='')
pm = PowerMonitor_keysight(rm.open_resource(fls_gpib), chan='1', slot=1)


calibration = SweepPolarization_SwitchPaths(fls, pol, pm, jds)

calibration.scantime = 5
calibration.range = [1, 2]
calibration.visual = True
calibration.verbose = True
calibration.visual = True
calibration.saveplot = True

file_name = '2022-08-31_SwitchPanelVerification'

sequence = calibration

input('***Press any key to begin calibration...***')
calibration.file_name = file_name + '-Calibration'
calibration.execute()

input('***Press any key to begin test....***')
sequence.file_name = file_name + '-Measurement'
sequence.execute()
'''
sequence.results.add('chip_id', chip_id)
sequence.results.add('die_id', die_id)
sequence.results.add('wafer_id', wafer_id)
sequence.results.add('lot_id', lot_id)
'''

calibration.results.save(calibration.file_name)
#sequence.results.save(f"{chip_id}_{die_id}_{device_id}")




pass
