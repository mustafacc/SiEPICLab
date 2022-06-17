# -*- coding: utf-8 -*-
"""
SiEPIClab application example: VOA measurement routine.

Mustafa Hammood, SiEPIC Kits, 2022
"""

import numpy as np
import pyvisa as visa
from siepiclab.instr import polCtrl_11896A, tls_keysight, pm_keysight
from siepiclab.experiment import exp, routine

rm = visa.ResourceManager()
# %% define the experiment
experiment = exp()

# %% define the experiment setup
tls = tls_keysight(rm.get_instrument('mainframe_1550'), channel='0')
polCtrl = polCtrl_11896A(rm.get_instrument('polCtrl'), channel='')
pd1 = pm_keysight(rm.get_instrument('mainframe_1550'), channel='1')

experiment = experiment.exp_setup([polCtrl, tls, pd1])

# %% define the experiment setup variables
wavlStart = 1500
wavlStop = 1580
wavlPts = 801
power_opt = 0 # 0 dBm = 1 mW

vStart = 0
vStop = 2
vPts = 51

vBiasPts = np.linspace(vStart, vStop, 4)
wavlCenter = (wavlStop-wavlStart)/2
# %% define the experiment routine
# typically the first step is moving the motors... 
# this example routine assumes device is probed

r = routine(experiment)

r.tls.WavlSet(wavlCenter)
r.tls.PwrSet(power_opt)

# %% execute the experiment
