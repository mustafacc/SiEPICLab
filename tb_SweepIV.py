"""
SiEPIClab testbench.

IV Sweep for the Keithley class source measure unit class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences.SweepIV import SweepIV
from siepiclab.drivers.smu_keithley import smu_keithley
rm = visa.ResourceManager()

# %% instruments definition
smu = smu_keithley(rm.open_resource('keithley_2602'))

# %% routine definition
sequence = SweepIV(smu)
sequence.v_start = 0
sequence.v_stop = 15
sequence.v_res = 0.1
sequence.chan = 'B'
sequence.verbose = True
sequence.visual = True
sequence.execute()
