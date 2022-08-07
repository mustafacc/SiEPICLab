"""
SiEPIClab sequence application example.

Sequence to perform swept wavelength measurement using tunable laser and monitor
at various voltage bias points.
Test setup:
    Optical:    laser -SMF-> ||DUT|| -SMF-> Power Monitor(s)
    Electrical: smu -GS-> ||DUT||

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences.SweepWavelengthSpectrum_VoltageBias import SweepWavelengthSpectrum_VoltageBias
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
from siepiclab.drivers.tls_keysight import tls_keysight
from siepiclab.drivers.lwmm_keysight import lwmm_keysight
from siepiclab.drivers.smu_keithley import smu_keithley
rm = visa.ResourceManager()

# %% instruments definition
mf = lwmm_keysight(rm.open_resource('mainframe_1550'))  # mainframe
tls = tls_keysight(rm.open_resource('mainframe_1550'), chan='0')
pm1 = PowerMonitor_keysight(rm.open_resource('mainframe_1550'), chan='1', slot='1')
pm2 = PowerMonitor_keysight(rm.open_resource('mainframe_1550'), chan='1', slot='2')
smu = smu_keithley(rm.open_resource('keithley_2602'))

# %% sequence definition
sequence = SweepWavelengthSpectrum_VoltageBias(mf, tls, [pm1, pm2], smu)
sequence.visual = True
sequence.verbose = True
sequence.upper_limit = -10
sequence.wavl_pts = 401
sequence.v_pts = [0, 1]
sequence.execute()
sequence.results.save()
