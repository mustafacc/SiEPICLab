"""
SiEPIClab testbench.

Testbench for the 11896A polarization controller class.

Mustafa Hammood, SiEPIC Kits, 2022
"""

# %%
import sys
sys.path.append(r'C:\Users\user\Documents\siepiclab')
sys.path.append(r'C:\Users\user\Documents\siepiclab\sequences')
sys.path.append(r'C:\Users\user\Documents\siepiclab\drivers')
# %%
import pyvisa as visa
import siepiclab as silab
rm = visa.ResourceManager()

# %% instruments definition
polCtrl = silab.drivers.PolCtrl_keysight(rm.get_instrument('PolCtrl-2'), chan='0')

# %% routine definition
paddlePosition = 401
paddlePositionAll = [123, 456, 789, 876]
scanrate = 4
routine = silab.routines.testbench_PolCtrl_keysight(polCtrl, paddlePosition, paddlePositionAll,
                                                    scanrate)
routine.execute()
