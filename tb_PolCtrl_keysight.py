"""
SiEPIClab testbench.

Testbench for the 11896A polarization controller class.

Mustafa Hammood, SiEPIC Kits, 2022
"""
# %%
import pyvisa as visa
from siepiclab.sequences import testbench_PolCtrl_keysight
from siepiclab.drivers import PolCtrl_keysight
rm = visa.ResourceManager()

# %% instruments definition
polCtrl = PolCtrl_keysight(rm.get_instrument('PolCtrl-2'), chan='0')

# %% sequence definition
sequence = testbench_PolCtrl_keysight(polCtrl)
sequence.execute(verbose=True)
