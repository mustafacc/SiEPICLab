# %%
"""
SiEPIClab measurement sequence.

On-Chip Laser Diode to On-Chip Photodiode (e.g. AIM, GF) Measurement Sequence.

Davin Birdi, 2024


# Experiment Setup:
LDC  -(elec probes)->   DUT [LD to PWB to waveguide to PD] -(elec probes)-> SMU


"""
import pyvisa as visa
from siepiclab import measurements

from siepiclab.drivers.ldc_srs_ldc500 import ldc_srs_ldc500
from siepiclab.drivers.smu_keithley2400 import smu_keithley2400

from time import sleep
import numpy as np

class onchipLDtoPD(measurements.sequence):
    """
    LD Biasing and PD Readout Sequence
    """
    
    def __init__(self, ldc, smu):
        super(onchipLDtoPD, self).__init__()

        self.ldc = ldc
        self.smu = smu

        # Default Settings: LDC
        self.Imin = 0
        self.Imax = 20
        self.numPts = 5 + 1
        
        # Default Settings: SMU
        self.v_bias = -1            # Volts:
        self.i_compliance = 10e-3   # Amps:

        # Lab Setup:
        self.instruments = [ldc, smu]
        self.experiment = measurements.lab_setup(self.instruments)

    def InstrSetting(self):
    
        smu.reset()

        # Set the Reverse Bias Voltage and the Compliance Current:
        self.smu.SetCurrentMode()

        #self.smu.
        self.smu.SetVoltage(self.v_bias)
        self.smu.SetCurrentLimit(self.i_compliance)

        # Set the TEC Beta and Ro Values:
        # TODO
        
        # 
         
        pass


    def instructions(self):
        
        if self.verbose:
            print('*** Setting Up Instrument: ***\n')
        self.InstrSetting()

        currentsSet=np.linspace(self.Imin,self.Imax,self.numPts)
        
        ld_currents=[]
        ld_voltages=[]

        pd_currents=[]
        pd_voltages=[]
    
        # Turn On Equipment:
        if self.verbose:
            print('***Activating TEC...***')
        self.ldc.tecON()
        
        if self.verbose:
            print('***Activating SMU...***')
        self.smu.SetOutput(True)
        
        if self.verbose:
            print('***Activating LD and Beginning Current Sweep...***')
        self.ldc.LDON()
        sleep(5)

        for ii, II in enumerate(currentsSet):
            self.ldc.SetLDcurrent(II)
            sleep(1)
            pd_currents = np.append(pd_currents, self.smu.GetCurrent())
            pd_voltages = np.append(pd_voltages, self.v_bias)
            
            ld_currents = np.append(ld_currents,self.ldc.GetLDcurrent())
            ld_voltages = np.append(ld_voltages,self.ldc.GetLDvoltage())
                
        if self.verbose:
            print('***Turning Off:***')
        self.ldc.SetLDcurrent(0)
        self.ldc.LDOFF()
        self.smu.SetOutput(False)

        sweepdata = measurements.results()


        sweepdata.add('pd_currents', pd_currents)
        sweepdata.add('pd_voltages', pd_voltages)

        sweepdata.add('ld_currents', ld_currents)
        sweepdata.add('ld_voltages', ld_voltages)

        self.results.add('sweepdata', sweepdata)

print('Hello World')

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import pandas as pd

    from datetime import datetime

    rm = visa.ResourceManager()


    ldc = ldc_srs_ldc500(rm.open_resource('ldc'))
    smu = smu_keithley2400(rm.open_resource('smu'))

    print(smu.identify())
    print(ldc.identify())
    

    
    
    
    
    sequence = onchipLDtoPD(ldc, smu)
    sequence.verbose = True

    # Setup the Sequence:
    test = False
    if test:
        # Sanity Check
        sequence.Imin = 0
        sequence.Imax = 10
        sequence.numPts = 3 + 1

    else:
        #Normal Settings
        sequence.Imin = 0
        sequence.Imax = 50
        sequence.numPts = 200 + 1

    sequence.v_bias = 1             # Volts:
    sequence.i_compliance = 10e-3   # Amps:

    sequence.execute()
    
    date = datetime.now().strftime("%y-%m-%d_%H-%M-%S")
    experiment_name = 'LDC-CurrentSweep_SMU-VoltageBias'
    
    measID = f'ARL_onchipIntegration_Sweep-{sequence.Imin}-{sequence.Imax}mA_Bias-{sequence.v_bias}V'
    basedir = 'C:\\Users\\dream\\OneDrive\\Documents\\dp_experiments\\ARL_onChipIntegration'
    savedir = basedir + '\\' + measID + '\\' + date + '\\'
    
    filename = savedir + measID
    sequence.results.createDir(savedir)

    measID = measID + '_hires'

    # Get the Data from the Sweep:
    sweepdata = sequence.results.data['sweepdata'].data

    # Save to CSV
    df = pd.DataFrame(sweepdata)    
    df.to_csv(filename + '.csv')
    
    # Plot and save as PNG
    fig, ax = plt.subplots(1,1)
    ax.plot(sweepdata['ld_currents'], 1e3*sweepdata['pd_currents'])
    ax.set_ylabel("PD Current mA")
    ax.set_xlabel("LD Current mA")
    fig.savefig(filename + '_plot.png')
# %%
