"""
SiEPIClab testbench.

Testbench for the a laser characterization routine using LDC501 and 81531A power monitor.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
import numpy as np
import time
import matplotlib.pyplot as plt
from siepiclab.sequences.testbench_PowerMonitor_keysight import testbench_PowerMonitor_keysight
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
from siepiclab.drivers.ldc_srs_ldc500 import ldc_srs_ldc500
rm = visa.ResourceManager()

# %% instruments definition
pm = PowerMonitor_keysight(rm.open_resource('GPIB2::22::INSTR'), chan='2')
ldc = ldc_srs_ldc500(rm.open_resource('GPIB2::3::INSTR'))
ldc.tecON()

# %% IV sweep definition
curr_min = 0
curr_max = 50
curr_range = np.arange(curr_min, curr_max, 0.1)

volt = []
curr = []
ldc.LDON()
time.sleep(5)
for i in curr_range:
    ldc.SetLDcurrent(i)
    time.sleep(0.1)
    volt.append(ldc.GetLDvoltage())
    curr.append(ldc.GetLDcurrent())

ldc.LDOFF()
#%%
plt.figure()
plt.plot(curr, volt)
plt.xlabel('Current [mA]')
plt.ylabel('Voltage [V]')
plt
# %% IV sweep definition
curr_min = 0
curr_max = 50
curr_range = np.arange(curr_min, curr_max, 0.1)

volt = []
curr = []
ldc.LDON()
time.sleep(5)
for i in curr_range:
    ldc.SetLDcurrent(i)
    time.sleep(0.1)
    volt.append(ldc.GetLDvoltage())
    curr.append(ldc.GetLDcurrent())

ldc.LDOFF()