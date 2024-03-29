"""
SiEPIClab testbench.

Testbench for the fixed laser source instrument class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences.testbench_fls_keysight import testbench_fls_keysight
from siepiclab.drivers.fls_keysight import fls_keysight
rm = visa.ResourceManager()

# %% instruments definition
mainframe_1550 = 'GPIB0::20::INSTR'
fls = fls_keysight(rm.open_resource(mainframe_1550), chan='2')

# %% routine definition
sequence = testbench_fls_keysight(fls)

sequence.verbose = True

sequence.execute()
