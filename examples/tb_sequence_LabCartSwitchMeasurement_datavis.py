"""
Data Visualization For LabCartSwitchMeasurement

"""

from siepiclab.measurements import sequence
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from ast import literal_eval

file_name = '2022-09-06_Device6-OnEachChannel'

meas = sequence().results.load(file_name)
cal = sequence().results.load(file_name + '_Calibration')

data = {}


for i in [1,2,3,4,5,6,7,8]:
    plt.figure(figsize=(11, 6))

    wavl = meas['wlsweep-chan'+str(i)][0]
    power_meas = 10*np.log10(meas['wlsweep-chan'+str(i)][1])
    power_cal  = 10*np.log10(cal['wlsweep-chan'+str(i)][1])

    measurement = (power_meas-power_cal)

    plt.plot(wavl, measurement)
    plt.xlim(min(wavl), max(wavl))
    plt.xlabel('Wavelength [nm]')
    plt.ylabel('Optical Power [dBm]')
    plt.legend(['CH'+str(i)])
    
    # Extract info from the Saved Results for Title:
    tls_info = literal_eval(meas['state_'+meas['instruments'][0]])
    plt.title(
        f"Result of Wavelength Spectrum Sweep.\nLaser power: {tls_info['pwr']} {tls_info['pwr_unit']}")
    plt.tight_layout()
    
    plt.savefig(str(file_name)+ '_chan' + str(i) + "_wavsweep_calibrated.png")

    # Need to output CSV of this!!!
    pass
    data.update({f'chan{i}': np.concatenate(measurement) })

out = pd.DataFrame.from_dict(data)
out.to_csv(file_name + '.csv', index=False)




# Overlay:
plt.figure(figsize=(11, 6))
legend_entries = []

for i in [1,2,3,4,5,6,7,8]:
    wavl = meas['wlsweep-chan'+str(i)][0]
    power_meas = 10*np.log10(meas['wlsweep-chan'+str(i)][1])
    power_cal  = 10*np.log10(cal['wlsweep-chan'+str(i)][1])

    plt.plot(wavl, power_meas - power_cal)
    legend_entries.append(f'CH{i}')

plt.xlim(min(wavl), max(wavl))
plt.xlabel('Wavelength [nm]')
plt.ylabel('Optical Power [dBm]')
plt.legend(legend_entries)

# Extract info from the Saved Results for Title:
tls_info = literal_eval(meas['state_'+meas['instruments'][0]])
plt.title(
    f"Result of Wavelength Spectrum Sweep.\nLaser power: {tls_info['pwr']} {tls_info['pwr_unit']}")
plt.tight_layout()

plt.savefig(str(file_name)+ "_Stacked.png")


