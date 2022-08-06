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
mf = lwmm_keysight(rm.open_resource('mainframe'))  # mainframe
tls = tls_keysight(rm.open_resource('mainframe'), chan='0')
pm1 = PowerMonitor_keysight(rm.open_resource('power_monitor'), chan='1')
pm2 = PowerMonitor_keysight(rm.open_resource('power_monitor'), chan='2')
# %% sequence definition
sequence = SweepWavelengthSpectrum(mf, tls, [pm1, pm2])
sequence.wavl_start = 1480  # nm
sequence.wavl_stop = 1580  # nm
sequence.wavl_pts = 1150  # number of points
sequence.pwr = 1  # mW
sequence.sweep_speed = 20  # nm/s
sequence.upper_limit = -10  # maximum power expected (dbm, -100: existing setting.)
sequence.verbose = True  # turn on verbose logging mode
sequence.visual = True  # visualize the wavelength sweep results

sequence.execute()
