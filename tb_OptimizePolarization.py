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

# %% routine definition

sequence = OptimizePolarization(fls, polCtrl, pm, scantime=5, verbose=True)
sequence.execute(verbose=True)
