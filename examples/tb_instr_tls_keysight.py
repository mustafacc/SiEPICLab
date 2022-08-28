"""
SiEPIClab testbench.

Testbench for the tunable laser source instrument class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences.testbench_tls_keysight import testbench_tls_keysight
from siepiclab.drivers.tls_keysight import tls_keysight
rm = visa.ResourceManager()

# %% instruments definition
mainframe_1550 = 'GPIB0::20::INSTR'
tls = tls_keysight(rm.open_resource(mainframe_1550), chan='2')

# %% sequence definition
sequence = testbench_tls_keysight(tls)
sequence.verbose = True
sequence.execute()
