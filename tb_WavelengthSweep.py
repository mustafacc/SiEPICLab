"""
SiEPIClab sequence application example.

Sequence to perform swept wavelength measurement using tunable laser and monitor.
Test setup:
    laser -SMF-> ||DUT|| -SMF-> Power Monitor(s)

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences import WavelengthSweep
from siepiclab.drivers import tls_keysight, PowerMonitor_keysight
rm = visa.ResourceManager()

# %% instruments definition
tls = tls_keysight(rm.get_instrument('mainframe_1550'), chan='0')
pm = PowerMonitor_keysight(rm.get_instrument('mainframe_1550'), chan='1')

# %% sequence definition
sequence = WavelengthSweep(tls, pm, verbose=True, visual=True)
sequence.wavlStart = 1280  # nm
sequence.wavlStop = 1380  # nm
sequence.wavlPts = 1001  # number of points
sequence.pwr = 1  # mW
sequence.sweepSpeed = 20  # nm/s
sequence.upperLimit = -20  # maximum power expected (dbm, -100: existing setting.)

sequence.execute(verbose=True)
