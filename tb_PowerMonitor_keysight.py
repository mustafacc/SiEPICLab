"""
SiEPIClab testbench.

Testbench for the 81635A optical power monitor class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences.testbench_PowerMonitor_keysight import testbench_PowerMonitor_keysight
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
rm = visa.ResourceManager()

# %% instruments definition
pm = PowerMonitor_keysight(rm.open_resource('power_monitor'), chan='1')

# %% routine definition
sequence = testbench_PowerMonitor_keysight(pm)
sequence.verbose = True
sequence.execute()
