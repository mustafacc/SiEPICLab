"""
SiEPIClab sequence application example.

Sequence to perform polarization sweep.
Test setup:
    laser -SMF-> polarization controller -SMF-> ||DUT|| -SMF-> Power Monitor

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences import SweepPolarization
from siepiclab.drivers.fls_keysight import fls_keysight
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
from siepiclab.drivers.PolCtrl_keysight import PolCtrl_keysight
rm = visa.ResourceManager()

# %% instruments definition
fls = fls_keysight(rm.open_resource('mainframe_1550'), chan='0')
polCtrl = PolCtrl_keysight(rm.open_resource('PolCtrl-2'), chan='0')
pm = PowerMonitor_keysight(rm.open_resource('mainframe_1550'), chan='1')

# %% sequence definition
sequence = SweepPolarization(fls, polCtrl, pm)

sequence.wavl = 1310
sequence.scantime = 5
sequence.scanrate = 1
sequence.optimize = True
sequence.verbose = True
sequence.visual = True

sequence.execute(verbose=True)

sequence.results.save()
