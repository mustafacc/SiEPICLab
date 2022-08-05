"""
SiEPIClab sequence application example.

Sequence to perform swept wavelength measurement using tunable laser and monitor.
Test setup:
    laser -SMF-> ||DUT|| -SMF-> Power Monitor(s)

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences.SweepWavelengthSpectrum import SweepWavelengthSpectrum
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
from siepiclab.drivers.tls_keysight import tls_keysight
from siepiclab.drivers.lwmm_keysight import lwmm_keysight
rm = visa.ResourceManager()

# %% instruments definition
mf = lwmm_keysight(rm.open_resource('mainframe_1550'))  # mainframe
tls = tls_keysight(rm.open_resource('mainframe_1550'), chan='0')
pm1 = PowerMonitor_keysight(rm.open_resource('mainframe_1550'), chan='2', slot='1')
pm2 = PowerMonitor_keysight(rm.open_resource('mainframe_1550'), chan='2', slot='2')
# %% sequence definition
sequence = SweepWavelengthSpectrum(mf, tls, [pm2])
sequence.wavlStart = 1280  # nm
sequence.wavlStop = 1370  # nm
sequence.wavlPts = 401  # number of points
sequence.pwr = 1  # mW
sequence.sweep_speed = 20  # nm/s
sequence.upper_limit = -10  # maximum power expected (dbm, -100: existing setting.)
sequence.verbose = True  # turn on verbose logging mode
sequence.visual = True  # visualize the wavelength sweep results

sequence.execute()
