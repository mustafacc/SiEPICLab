"""
SiEPIClab testbench.

Testbench for the 11896A polarization controller class.

Mustafa Hammood, SiEPIC Kits, 2022
"""

# %%
import sys
sys.path.append(r'C:\Users\user\Documents\siepiclab')
sys.path.append(r'C:\Users\user\Documents\siepiclab\routines')
# %%
import pyvisa as visa
import siepiclab as silab
rm = visa.ResourceManager()

# %% instruments definition
polCtrl = silab.instruments.PolCtrl_keysight(rm.get_instrument('PolCtrl-2'), chan='0')

# %% routine definition
routine = silab.routines.testbench_PolCtrl_keysight.testbench(polCtrl, 900)
routine.execute()
