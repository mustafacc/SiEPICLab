"""
SiEPIClab testbench routine.

Routine to characterize a photodiode.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
import numpy as np
from siepiclab.measurements import routine
from siepiclab.sequences.SweepIV_opticalinput import SweepIV_opticalinput
from siepiclab.sequences.PD_Responsivity import PD_Responsivity
from siepiclab.drivers.smu_keithley import smu_keithley
from siepiclab.drivers.tls_keysight import tls_keysight
rm = visa.ResourceManager()

# %% instruments definition
smu = smu_keithley(rm.open_resource('keithley_2602'))
tls = tls_keysight(rm.open_resource('mainframe_1550'), chan='0')
# %% routine definition
routine = routine()

sequence = SweepIV_opticalinput(smu, tls)
v_min = -1
v_max = 0.5
v_res = 0.01
sequence.v_pts = np.arange(v_min, v_max, v_res)
sequence.chan = 'B'
sequence.verbose = True
sequence.visual = True

#routine.add(sequence)
