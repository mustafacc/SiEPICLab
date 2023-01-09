"""
SiEPIClab measurement sequence.

LDC Setup and current sweep sequence.

Davin Birdi, UBC Photonics, 2022

@original author: Hossam Shoman, 2018
@modified: Iman Taghavi, 2021
"""
from siepiclab import measurements
import numpy as np
import matplotlib.pyplot as plt 
from datetime import datetime
from time import sleep



class SetupLDC501(measurements.sequence):
    """
    Current sweep sequence.
    """

    def __init__(self, ldc, pm):
        super(SetupLDC501, self).__init__()
        self.ldc = ldc
        self.pm = pm

        self.Imin=5
        self.Imax=15
        self.numPts=3

        self.temperature=25

        self.instruments = [ldc, pm]
        self.experiment = measurements.lab_setup(self.instruments)

         # TEC Settings:
        self.ldc.tecMode('CT')
        self.ldc.SetTemperature(self.temperature)
    
        # Power Monitor Settings:
        self.pm.SetWavl(1270)
        self.pm.SetPwrUnit('mw')



    def InstrSetting(self):
        pass


    def instructions(self):
        
        if self.verbose:
            print('*** Setting Up Instrument: ***\n')
        self.InstrSetting()

        # Setup 

        #%% LIV sweep using the LDC and large area PD
        currentsSet=np.linspace(self.Imin,self.Imax,self.numPts)
        currents=[]
        voltages=[]
        powers=[]
        powersdbm=[]

        if self.verbose:
            print('***Activating TEC...***')
        self.ldc.tecON()
        if self.verbose:
            print('***Activating LD and Beginning Current Sweep...***')
        self.ldc.LDON()
        sleep(5)
        for ii, II in enumerate(currentsSet):
            self.ldc.SetLDcurrent(II)
            sleep(1)
            powers = np.append(powers,self.pm.GetPwr())
            powersdbm = np.append(powersdbm,self.pm.GetPwr(True))
            currents = np.append(currents,self.ldc.GetLDcurrent())
            voltages = np.append(voltages,self.ldc.GetLDvoltage())
        
        if self.verbose:
            print('***Turning Off LD:***')
        self.ldc.SetLDcurrent(0)
        self.ldc.LDOFF()

        self.results.add('currents', currents)
        self.results.add('voltages', voltages)
        self.results.add('powers', powers)
        self.results.add('powersdbm', powersdbm)
        

        
        #%% 
        if self.visual or self.saveplot == True:
            #filename=(datetime.now().strftime('%Y%m%d%H%M%S')+'_Isweep')  
            filename = self.file_name

            plt.close(1)
            plt.figure(1, figsize=(11, 6))
            plt.plot(currents,voltages,'.k', label = 'Data')
            plt.ylabel('Voltage (V)')
            plt.xlabel('Current (mA)')
            title1 = str(self.file_name) + 'LDC Current Sweep Sequence\n'
            title2 = f'Voltage vs. Current Sweep from {self.Imin} to {self.Imax}' + '\n'
            title3 = f'Temperature = {int(self.temperature)} degC'
            plt.title(title1+title2+title3) 
            plt.tight_layout()   
            if self.saveplot:
                plt.savefig(filename+'_IV.png')
            if not(self.visual):
                plt.close(1)
            
            
            plt.close(2)
            plt.figure(2, figsize=(11, 6))
            plt.plot(currents,powers,'.k', label = 'Data')
            plt.ylabel('Power (mW)')
            plt.xlabel('Current (mA)')
            title1 = str(self.file_name) + 'LDC Current Sweep Sequence\n'
            title2 = f'Optical Power vs. Current Sweep from {self.Imin} to {self.Imax}\n'
            title3 = f'Temperature = {int(self.temperature)} degC'
            plt.title(title1+title2+title3) 
            plt.tight_layout()   
            if self.saveplot:
                plt.savefig(filename+'_LI(mW).png')
            if not(self.visual):
                plt.close(2)
                

            plt.close(3)
            plt.figure(3, figsize=(11, 6))
            plt.plot(currents,powersdbm,'.k', label = 'Data')
            plt.ylabel('Power (dBm)')
            plt.xlabel('Current (mA)')
            title1 = str(self.file_name) + 'LDC Current Sweep Sequence\n'
            title2 = f'Optical Power vs. Current Sweep from {self.Imin} to {self.Imax}\n'
            title3 = f'Temperature = {int(self.temperature)} degC'
            plt.title(title1+title2+title3)
            plt.tight_layout()    
            if self.saveplot:
                plt.savefig(filename+'_LI(db).png')
            if not(self.visual):
                plt.close(3)

        
        if self.verbose:
            print('\n***Sequence Complete! Exiting...***')

        pass



       
        