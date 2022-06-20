"""
SiEPIClab sequence application example.

Sequence to perform polarization optimization.
Test setup:
    laser -SMF-> polarization controller -SMF-> ||DUT|| -SMF-> Power Monitor

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences import OptimizePolarization
from siepiclab.drivers import fls_keysight, PowerMonitor_keysight, PolCtrl_keysight
rm = visa.ResourceManager()

# %% instruments definition
fls = fls_keysight(rm.get_instrument('mainframe_1550'), chan='0')
polCtrl = PolCtrl_keysight(rm.get_instrument('PolCtrl-2'), chan='0')
pm = PowerMonitor_keysight(rm.get_instrument('mainframe_1550'), chan='1')

# %% sequence definition
sequence = OptimizePolarization(fls, polCtrl, pm)

sequence.wavl = 1310
sequence.scantime = 5
sequence.scanrate = 1
sequence.verbose = True
sequence.visual = True

sequence.execute(verbose=True)
