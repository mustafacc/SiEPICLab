# -*- coding: utf-8 -*-

"""
SiEPIClab sequence application example.

Sequence to perform IV Characterization of Laser.
Test setup:
    LDC501 -BNC-> || DUT || -SMF-> Power Monitor

Davin Birdi, 2022
With Templates and support from Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences.SetupLDC501 import SetupLDC501
from siepiclab.drivers.ldc_srs_ldc500 import ldc_srs_ldc500
from siepiclab.drivers.PowerMonitor_keysight import PowerMonitor_keysight
rm = visa.ResourceManager()


# %% instruments definition
print(rm.list_resources())
def searchList(mylist, mystr):
    for i in range(0,len(mylist)):
        if mystr in mylist[i]:
            return mylist[i]
    raise NameError('The Instrument Number you Specified is not in the Available GPIB Resources')


ldc = ldc_srs_ldc500(rm.open_resource(searchList(rm.list_resources(), "::2::")), chan='1')
pm = PowerMonitor_keysight(rm.open_resource(searchList(rm.list_resources(), "::20::")), chan='1')

# %% sequence definition
sequence = SetupLDC501(ldc, pm)
#sequence.visual = True
sequence.execute()
sequence.results.save(file_name='test')


pass

# %%
