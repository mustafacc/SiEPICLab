"""
SiEPIClab measurement sequence.

On-Chip Laser Diode to On-Chip Photodiode (e.g. AIM, GF) Measurement Sequence.

Davin Birdi, 2024


# Experiment Setup:
LDC  -(elec probes)->   DUT [LD to PWB to waveguide to PD] -(elec probes)-> SMU


"""
import pyvisa as visa
from siepiclab import measurements

from siepiclab.drivers import ldc_srs_ldc500
from siepiclab.drivers import smu_keithley2400




class onchipLDtoPD(measurements.sequence):
    """
    LD Biasing and PD Readout Sequence
    """
    
    def __init__(self, ldc, smu):
        super(onchipLDtoPD, self).__init__()

        self.ldc = ldc
        self.smu = smu



if __name__ == '__main___':
    rm = visa.ResourceManager()


    ldc = ldc_srs_ldc500(rm.open_resource('GPIB0::20::INSTR'))
    smu = smu_keithley2400(rm.open_resource('GPIB0::20::INSTR'))

    print(smu.identify())
    print(ldc.identify())