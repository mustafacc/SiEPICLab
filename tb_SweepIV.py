"""
SiEPIClab testbench.

IV Sweep for the Keithley class source measure unit class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
import numpy as np
from siepiclab.sequences.SweepIV import SweepIV
from siepiclab.drivers.smu_keithley import smu_keithley
rm = visa.ResourceManager()

# %% instruments definition
smu = smu_keithley(rm.open_resource('keithley_2602'))

# %% routine definition
v_min = 0
v_max = 1
v_res = 0.05

sequence = SweepIV(smu)
sequence.v_pts = np.arange(v_min, v_max, v_res)
sequence.chan = 'B'
sequence.verbose = True
sequence.visual = True
sequence.execute()
