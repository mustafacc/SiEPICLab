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

        #self.ldc = ldc
        #self.smu = smu
        self.ldc = ldc_srs_ldc500()
        self.smu = smu_keithley2400()


        self.Imin = 0
        self.Imax = 10
        self.numPts = 2 + 1

        # Default Settings:
        self.v_bias = -1              # Volts:
        self.i_compliance = 10e-3   # Amps:

        # Lab Setup:
        self.instruments = [ldc, smu]
        self.experiment = measurements.lab_setup(self.instruments)

    def InstrSetting(self):
    
        # Set the Reverse Bias Voltage and the Compliance Current:
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
    

        if self.verbose:
            print('***Activating TEC...***')
        self.ldc.tecON()
        if self.verbose:
            print('***Activating LD and Beginning Current Sweep...***')
        self.ldc.LDON()
        sleep(5)

        for ii, II in enumerate(currentsSet):
            self.ldc.SetLDcurrent(II)
            sleep(2)
            pd_currents = np.append(pd_currents, self.smu.GetCurrent())
            pd_voltages = np.append(pd_voltages, self.smu.GetCurrent())
            
            ld_currents = np.append(ld_currents,self.ldc.GetLDcurrent())
            ld_voltages = np.append(ld_voltages,self.ldc.GetLDvoltage())
                
        if self.verbose:
            print('***Turning Off LD:***')
        self.ldc.SetLDcurrent(0)
        self.ldc.LDOFF()


        self.results.add('pd_currents', pd_currents)
        self.results.add('pd_voltages', pd_voltages)
        self.results.add('ld_currents', ld_currents)
        self.results.add('ld_voltages', ld_voltages)



if __name__ == '__main___':
    rm = visa.ResourceManager()


    ldc = ldc_srs_ldc500(rm.open_resource('GPIB0::20::INSTR'))
    smu = smu_keithley2400(rm.open_resource('GPIB0::20::INSTR'))

    print(smu.identify())
    print(ldc.identify())
    
    sequence = onchipLDtoPD(ldc, smu)
