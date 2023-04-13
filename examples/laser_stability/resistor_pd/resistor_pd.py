# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 15:01:41 2023

@author: user
"""

import pyvisa as visa
from siepiclab.drivers.smu_keithley import smu_keithley
from datetime import datetime
import yaml
import os

rm = visa.ResourceManager()
# %% instruments definition
smu = smu_keithley(rm.open_resource('GPIB2::10::INSTR'))

# %%
# sweep resistor and measure pd photocurrent over an infinite loop
ch_ps='A'
ch_pd='B'
v_ps_start=0
v_ps_stop=5
v_pd_bias=-2
pts=100

# %%
# Define the subdirectory
subdirectory = datetime.now().date()

f_name1 = str(datetime.now().date()).replace('-', '_')
f_name2 = str(datetime.now().time()).replace('.', '_').replace(':', '_')

subdirectory = f_name1 + '_' + f_name2

# Create the subdirectory if it doesn't exist
os.makedirs(subdirectory, exist_ok=True)

smu.reset()
while True:
    # run the measurement routine
    data = smu.SweepVV_independent(ch1=ch_ps, ch2=ch_pd, v1_start=v_ps_start,
                            v1_stop=v_ps_stop, v2_bias=v_pd_bias, pts=pts, visualize=False)

    f_name2 = str(datetime.now().time()).replace('.', '_').replace(':', '_')

    # save data to yaml
    yaml_file_path = os.path.join(subdirectory, f'{f_name2}.yaml')
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump([list(i) for i in data], yaml_file)

# %% Example: Read the contents of the YAML file
import matplotlib.pyplot as plt

with open(yaml_file_path, 'r') as yaml_file:
    [v1, i1, v2, i2] = yaml.safe_load(yaml_file)

fig1, ax1 = plt.subplots()
ax1.plot(v1, i1, label='CH1 (PS)', color='blue')
ax1.set_xlabel('Voltage CH1 (V)', color='blue')
ax1.set_ylabel('Current CH1 (A)', color='blue')
ax1.set_title(f'sweep_2CH_independent. CH1')
fig1.show()

fig2, ax2 = plt.subplots()
ax2.plot(v2, i2, label='CH2 (PD)', color='red')
ax2.set_xlabel('Voltage CH2 (V)', color='red')
ax2.set_ylabel('Current CH1 (A)', color='red')
ax1.set_title(f'sweep_2CH_independent. CH2')
fig2.show()