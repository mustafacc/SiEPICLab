"""
SiEPIClab testbench.

Testbench for the 81635A optical power monitor class.

Mustafa Hammood, SiEPIC Kits, 2022
"""

# %%
import sys
sys.path.append(r'C:\Users\user\Documents\siepiclab')
sys.path.append(r'C:\Users\user\Documents\siepiclab\sequences')
sys.path.append(r'C:\Users\user\Documents\siepiclab\drivers')
# %%
import pyvisa as visa
from siepiclab.sequences import testbench_fls_keysight
from siepiclab.drivers import fls_keysight
rm = visa.ResourceManager()

# %% instruments definition
fls = fls_keysight(rm.get_instrument('mainframe_1550'), chan='0')

# %% routine definition
sequence = testbench_fls_keysight(fls)
sequence.execute()
