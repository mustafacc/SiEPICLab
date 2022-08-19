"""
SiEPIClab testbench.

Basic Testbench toggling through switch outputs.

Davin Birdi, UBC Photonics

With Credit to:
Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
import numpy as np
from siepiclab.sequences.SwitchPath import SwitchPath
from siepiclab.drivers.opticalSwitch_jds import opticalSwitch_jds
from random import randint

rm = visa.ResourceManager()
print(rm.list_resources())
# %% instruments definition

switch_gpib = 'GPIB0::7::INSTR'
switch_gpib = 'visa://10.2.137.163/GPIB0::7::INSTR'
jds = opticalSwitch_jds(rm.open_resource(switch_gpib), chan='')


sequence = SwitchPath(jds)

sequence.chan = randint(1,8)

sequence.execute()

pass
