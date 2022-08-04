"""
SiEPIClab sequence application example.

Sequence to perform swept wavelength measurement using tunable laser and monitor.
Test setup:
    laser -SMF-> ||DUT|| -SMF-> Power Monitor(s)

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences import SweepWavelength
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
from siepiclab.drivers.tls_keysight import tls_keysight
rm = visa.ResourceManager()

# %% instruments definition
tls = tls_keysight(rm.open_resource('mainframe_1550'), chan='0')
pm = PowerMonitor_keysight(rm.open_resource('mainframe_1550'), chan='1')

# %% sequence definition
sequence = SweepWavelength(tls, pm)
sequence.wavlStart = 1280  # nm
sequence.wavlStop = 1380  # nm
sequence.wavlPts = 1001  # number of points
sequence.pwr = 1  # mW
sequence.sweepSpeed = 20  # nm/s
sequence.upperLimit = -20  # maximum power expected (dbm, -100: existing setting.)
sequence.verbose = True
sequence.visual = True

sequence.execute(verbose=True)
