"""
SiEPIClab testbench.

Testbench for the keithley 2400 class source measure unit class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences.testbench_smu_keithley2400 import testbench_smu_keithley2400
from siepiclab.drivers.smu_keithley2400 import smu_keithley2400
rm = visa.ResourceManager()

# %% instruments definition
smu = smu_keithley2400(rm.open_resource('GPIB2::11::INSTR'))

# %% routine definition
sequence = testbench_smu_keithley2400(smu)
sequence.verbose = True
sequence.execute()
