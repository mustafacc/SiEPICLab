"""
Created on Fri Jun 17 11:33:15 2022.

@author: siepiclab testbench.
"""
# %%
import pyvisa as visa
import siepiclab as silab

# %% instruments definition
rm = visa.ResourceManager()

pm = silab.instruments.PowerMonitor_keysight(
    rm.get_instrument('mainframe_1550'), chan='1')

polCtrl = silab.instruments.PolCtrl_keysight(rm.get_instrument('PolCtrl-2'), chan='0')

# %% routine definition
routine = silab.measurements.TestRoutine(polCtrl, 100)