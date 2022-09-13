"""
SiEPIClab sequence application example.

Sequence to perform swept wavelength measurement using compact tunable laser (81689A) and monitor.
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
mainframe_1550 = 'GPIB0::20::INSTR'
mf = lwmm_keysight(rm.open_resource(mainframe_1550))  # mainframe
tls = tls_keysight(rm.open_resource(mainframe_1550), chan='2')
pm1 = PowerMonitor_keysight(rm.open_resource(mainframe_1550), chan='1', slot='1')
pm2 = PowerMonitor_keysight(rm.open_resource(mainframe_1550), chan='1', slot='1')
# %% sequence definition
sequence = SweepWavelengthSpectrum(mf, tls, [pm1,pm2])
sequence.wavl_start = 1524  # nm
sequence.wavl_stop = 1575  # nm
sequence.wavl_pts = 101  # number of points
sequence.pwr = 1  # mW
sequence.sweep_speed = 40  # nm/s
sequence.upper_limit = -1  # maximum power expected (dbm, -100: existing setting.)
sequence.verbose = True  # turn on verbose logging mode
sequence.visual = True  # visualize the wavelength sweep results
sequence.saveplot = True
sequence.mode = 'step'  # use stepped mode instead of continuous

file_name = '2022-08-23_test3'
sequence.file_name = file_name

sequence.execute()
sequence.results.save(file_name)
pass
