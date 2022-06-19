"""
SiEPIClab testbench.

Testbench for the tunable laser source instrument class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences import testbench_tls_keysight
from siepiclab.drivers import tls_keysight
rm = visa.ResourceManager()

# %% instruments definition
tls = tls_keysight(rm.get_instrument('mainframe_1550'), chan='0')

# %% routine definition
sequence = testbench_tls_keysight(tls)
sequence.execute(verbose=True)
