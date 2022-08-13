"""
SiEPIClab testbench.

IV Sweep for the Keithley class source measure unit class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences.PD_Responsivity import PD_Responsivity
from siepiclab.drivers.smu_keithley import smu_keithley
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
from siepiclab.drivers.tls_keysight import tls_keysight
rm = visa.ResourceManager()

# %% instruments definition
smu = smu_keithley(rm.open_resource('keithley_2604b'))
pm = PowerMonitor_keysight(rm.open_resource('mainframe_1550'), chan='1', slot='2')
tls = tls_keysight(rm.open_resource('mainframe_1550'), chan='0')
# %% routine definition

sequence = PD_Responsivity(smu, pm, tls)
sequence.smu_v_bias = [0, -2]
sequence.smu_chan = 'B'

sequence.wavl_start = 1300
sequence.wavl_stop = 1320
sequence.wavl_pts = 100
sequence.laser_pwr = 9
sequence.loss_coupling = 6

sequence.verbose = True
sequence.visual = True
sequence.saveplot = True
sequence.execute()

sequence.results.save()
