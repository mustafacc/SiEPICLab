"""
SiEPIClab testbench.

Testbench for the 81635A optical power monitor class.

Mustafa Hammood, SiEPIC Kits, 2022
"""

# %%
import sys
sys.path.append(r'C:\Users\user\Documents\siepiclab')
sys.path.append(r'C:\Users\user\Documents\siepiclab\routines')
sys.path.append(r'C:\Users\user\Documents\siepiclab\drivers')
# %%
import pyvisa as visa
import siepiclab as silab
rm = visa.ResourceManager()

# %% instruments definition
pm = silab.drivers.PowerMonitor_keysight(rm.get_instrument('mainframe_1550'), chan='1')

# %% routine definition

routine = silab.routines.testbench_PowerMonitor_keysight(pm)
routine.execute()
