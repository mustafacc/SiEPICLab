"""
SiEPIClab testbench.

Testbench for the Keithley class source measure unit class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences.testbench_smu_keithley import testbench_smu_keithley
from siepiclab.drivers.smu_keithley import smu_keithley
rm = visa.ResourceManager()

# %% instruments definition
smu = smu_keithley(rm.open_resource('keithley_2602'), chan='0')

# %% routine definition
sequence = testbench_smu_keithley(smu)
sequence.execute(verbose=True)
