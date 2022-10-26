"""
SiEPIClab testbench.

IV Sweep for the Keithley class source measure unit class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
import numpy as np
from siepiclab.sequences.SweepIV_opticaloutput import SweepIV_opticaloutput
from siepiclab.drivers.smu_keithley import smu_keithley
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
rm = visa.ResourceManager()

# %% instruments definition
smu = smu_keithley(rm.open_resource('keithley_2604b'))
pm1 = PowerMonitor_keysight(rm.open_resource('mainframe_1550'), chan='1', slot='2')
# %% routine definition
v_min = 0
v_max = .5
v_res = 0.01

sequence = SweepIV_opticaloutput(smu, [pm1])
sequence.v_pts = np.arange(v_min, v_max, v_res)
sequence.chan = 'B'
sequence.pwr_lim = 60e-3
sequence.volt_lim = 4
sequence.curr_lim = 30e-3
sequence.verbose = True
sequence.visual = True
sequence.execute()

sequence.results.save()
