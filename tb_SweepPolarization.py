"""
SiEPIClab sequence application example.

Sequence to perform polarization sweep.
Test setup:
    laser -SMF-> polarization controller -SMF-> ||DUT|| -SMF-> Power Monitor

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences import SweepPolarization
from siepiclab.drivers import fls_keysight, PowerMonitor_keysight, PolCtrl_keysight
rm = visa.ResourceManager()


# %% instruments definition
'''
fls = fls_keysight(rm.get_instrument('mainframe_1550'), chan='0')
polCtrl = PolCtrl_keysight(rm.get_instrument('PolCtrl-2'), chan='0')
pm = PowerMonitor_keysight(rm.get_instrument('mainframe_1550'), chan='1')
'''

# %% instruments definition
print(rm.list_resources())
def searchList(mylist, mystr):
    for i in range(0,len(mylist)):
        if mystr in mylist[i]:
            return mylist[i]
    raise NameError('The Instrument Number you Specified is not in the Available GPIB Resources')


fls = fls_keysight(rm.open_resource(searchList(rm.list_resources(), "::20::")), chan='0')
polCtrl = PolCtrl_keysight(rm.open_resource(searchList(rm.list_resources(), "::8::")), chan='0')
pm = PowerMonitor_keysight(rm.open_resource(searchList(rm.list_resources(), "::20::")), chan='1')

# %% sequence definition
sequence = SweepPolarization(fls, polCtrl, pm)

sequence.wavl = 1550
sequence.scantime = 45
sequence.scanrate = 1
sequence.optimize = True
sequence.verbose = True
sequence.visual = True

sequence.execute(verbose=True)
