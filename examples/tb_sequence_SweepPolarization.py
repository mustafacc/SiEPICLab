"""
SiEPIClab sequence application example.

Sequence to perform polarization sweep.
Test setup:
    laser -SMF-> polarization controller -SMF-> ||DUT|| -SMF-> Power Monitor

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
from tkinter import N
import pyvisa as visa
from siepiclab.sequences.SweepPolarization import SweepPolarization
from siepiclab.drivers.fls_keysight import fls_keysight
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
from siepiclab.drivers.PolCtrl_keysight import PolCtrl_keysight
rm = visa.ResourceManager()


# %% instruments definition

if False:
    mf_gpib = 'GPIB0::20::INSTR'
    pol_gpib = 'GPIB0::8::INSTR'
else:
    mf_gpib = 'visa://10.2.137.163/GPIB0::20::INSTR'
    pol_gpib = 'visa://10.2.137.163/GPIB0::8::INSTR'



fls = fls_keysight(rm.open_resource(mf_gpib), chan='2')
polCtrl = PolCtrl_keysight(rm.open_resource(pol_gpib), chan='0')
pm = PowerMonitor_keysight(rm.open_resource(mf_gpib), chan='1', slot=2)

# %% sequence definition
sequence = SweepPolarization(fls, polCtrl, pm)

sequence.wavl = 1550
sequence.scantime = 45
sequence.scanrate = 1

sequence.optimize = True
sequence.verbose = True
sequence.visual = True
sequence.saveplot = True

file_name = '2022-08-26_ANT1_postAPCIncident_Fixed_NewLoopback'
#sequence.file_name = '2022-08-25_ANT1-Zeroing'

idx = 0
while True:
    sequence.file_name = str(file_name) + "-run" + str(idx)
    sequence.execute()


    #sequence.results.save(sequence.file_name)
    maxT = sequence.results.data['maxT']
    print(maxT) 
    # Save Results to a file:
    with open(file_name+ '.txt', 'a') as f:
        f.write(str(maxT) + ', ')
    
    if input("Do again? [Y] or [N]").lower() == 'n':
        break

print('Experiment done.')



