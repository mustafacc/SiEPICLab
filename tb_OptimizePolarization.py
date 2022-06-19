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
wavl = 1310
scantime = 5
scanrate = 1

sequence = OptimizePolarization(fls, polCtrl, pm, wavl=wavl, scantime=scantime,
                                scanrate=scanrate, verbose=True, visual=True)
sequence.execute(verbose=True)
