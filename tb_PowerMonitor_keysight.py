"""
SiEPIClab testbench.

Testbench for the 81635A optical power monitor class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences import testbench_PowerMonitor_keysight
from siepiclab.drivers import PowerMonitor_keysight
rm = visa.ResourceManager()

# %% instruments definition
pm = PowerMonitor_keysight(rm.get_instrument('mainframe_1550'), chan='1')

# %% routine definition
sequence = testbench_PowerMonitor_keysight(pm)
sequence.execute(verbose=True)
