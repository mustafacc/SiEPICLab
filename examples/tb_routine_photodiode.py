"""
SiEPIClab testbench routine.

Routine to characterize a photodiode.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
import numpy as np
from siepiclab.sequences.SweepIV_photodiode import SweepIV_photodiode
from siepiclab.sequences.PD_Responsivity import PD_Responsivity
from siepiclab.drivers.smu_keithley import smu_keithley
from siepiclab.drivers.tls_keysight import tls_keysight
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
rm = visa.ResourceManager()

# %% instruments definition
smu = smu_keithley(rm.open_resource('keithley_2604b'))
tls = tls_keysight(rm.open_resource('mainframe_1550'), chan='0')
pm1 = PowerMonitor_keysight(rm.open_resource('mainframe_1550'), chan='1', slot='2')
# %% routine definition
chip_id = 'AIM_DP_21_05'
die_id = '13'
lot_id = '2202AMPM002.003'
wafer_id = '7D5Df069SOA0'
device_id = 'drp_o_power_monitor_te_se'

sequence = SweepIV_photodiode(smu, tls, pm1)
v_min = -2
v_max = .5
v_res = 0.01

sequence.laser_pwr = [0]  # mW
sequence.laser_wavl = 1310  # nm
sequence.v_pts = np.arange(v_min, v_max, v_res)
sequence.chan = 'B'
sequence.verbose = True
sequence.visual = True
sequence.saveplot = True

sequence.execute()

# %%
