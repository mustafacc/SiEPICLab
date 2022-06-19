"""
SiEPIClab testbench.

Testbench for the fixed laser source instrument class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences import testbench_fls_keysight
from siepiclab.drivers import fls_keysight
rm = visa.ResourceManager()

# %% instruments definition
fls = fls_keysight(rm.get_instrument('mainframe_1550'), chan='0')

# %% routine definition
sequence = testbench_fls_keysight(fls)
sequence.execute(verbose=True)
