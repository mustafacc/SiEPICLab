"""
SiEPIClab testbench.

IV Sweep for the Keithley class source measure unit class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
import numpy as np
from siepiclab.sequences.SweepIV_optical import SweepIV_optical
from siepiclab.drivers.smu_keithley import smu_keithley
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
rm = visa.ResourceManager()

# %% instruments definition
smu = smu_keithley(rm.open_resource('keithley_2604b'))
pm1 = PowerMonitor_keysight(rm.open_resource('mainframe_1550'), chan='1', slot='2')
# %% routine definition
chip_id = 'AIM_DP_21_05'
die_id = '12'
wafer_id = '2202AMPM002.003'
lot_id = '7D5Df069SOA0'
device_id = 'drp_cl_phase_shifter_thermal_compact_te_se'

resistance = 250  # ohms (assumption)
p_min = 0  # mW
p_max = 500e-3  # mW
p_res = .1e-3  # mW
p_range = np.arange(p_min, p_max, p_res)

sequence = SweepIV_optical(smu, [pm1])
sequence.v_pts = np.sqrt(p_range*resistance)  # sample linearly in power not in voltage
sequence.chan = 'B'
sequence.pwr_lim = 1000e-3
sequence.volt_lim = 20
sequence.curr_lim = 85e-3
sequence.verbose = True
sequence.visual = True
sequence.saveplot = True
sequence.execute()

sequence.results.add('chip_id', chip_id)
sequence.results.add('die_id', die_id)
sequence.results.add('wafer_id', wafer_id)
sequence.results.add('lot_id', lot_id)
sequence.results.save(f"{chip_id}_{die_id}_{device_id}")
