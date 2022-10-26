"""
SiEPIClab testbench.

IV Sweep for the Keithley class source measure unit class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
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
device_id = 'drp_cl_voa_efficient_te_se'

v_min = 0  # V
v_max = 1  # V
v_res = .005  # V
v_range = np.arange(v_min, v_max, v_res)

sequence = SweepIV_optical(smu, [pm1])
sequence.v_pts = v_range
sequence.chan = 'B'
sequence.pwr_lim = 1000e-3
sequence.volt_lim = 5
sequence.curr_lim = 400e-3
sequence.verbose = True
sequence.visual = True
sequence.saveplot = True
sequence.execute()

# %% extract the attenuation vs voltage/E-pwr
pwr_optical = 10*np.log10(sequence.results.data['pwr_optical'])
attenuation = pwr_optical-np.max(pwr_optical)
volt = sequence.results.data['volt']
curr = sequence.results.data['curr']


plt.figure(figsize=(11, 6))
plt.plot(volt, attenuation, '.')
plt.xlabel('Voltage [V]')
plt.ylabel('Optical attenuation [dB]')
plt.title(f"{chip_id}_{die_id}_{device_id}")
plt.tight_layout()
plt.savefig(f"{chip_id}_{die_id}_{device_id}_OPWR_V.pdf")

plt.figure(figsize=(11, 6))
plt.plot(volt*curr*1e3, attenuation, '.')
plt.xlabel('Electrical power [mW]')
plt.ylabel('Optical attenuation [dB]')
plt.title(f"{chip_id}_{die_id}_{device_id}")
plt.tight_layout()
plt.savefig(f"{chip_id}_{die_id}_{device_id}_OPWR_EPWR.pdf")

sequence.results.add('chip_id', chip_id)
sequence.results.add('die_id', die_id)
sequence.results.add('wafer_id', wafer_id)
sequence.results.add('lot_id', lot_id)
sequence.results.save(f"{chip_id}_{die_id}_{device_id}")
