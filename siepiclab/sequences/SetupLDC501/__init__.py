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

        self.instruments = [ldc, pm]
        self.experiment = measurements.lab_setup(self.instruments)



    def InstrSetting(self):
        
        # TEC Settings:
        self.ldc.tecMode('CT')
        self.ldc.SetTemperature(25)
    
        # Power Monitor Settings:
        self.pm.SetWavl(1270)
        self.pm.SetPwrUnit('mw')


    def instructions(self):
        
        self.InstrSetting()

        # Setup 

        #%% LIV sweep using the LDC and large area PD
        Imin=5
        Imax=15
        numPts=3
        currentsSet=np.linspace(Imin,Imax,numPts)
        currents=[]
        voltages=[]
        powers=[]
        powersdbm=[]

        self.ldc.LDON()
        for ii, II in enumerate(currentsSet):
            self.ldc.SetLDcurrent(II)
            sleep(2)
            powers = np.append(powers,self.pm.GetPwr())
            powersdbm = np.append(powersdbm,self.pm.GetPwr(True))
            currents = np.append(currents,self.ldc.GetLDcurrent())
            voltages = np.append(voltages,self.ldc.GetLDvoltage())
        self.ldc.SetLDcurrent(0)
        self.ldc.LDOFF()

        self.results.add('currents', currents)
        self.results.add('voltages', voltages)
        self.results.add('powers', powers)
        self.results.add('powersdbm', powersdbm)
        

        
        #%% 
        if self.visual == True:
            filename=(datetime.now().strftime('%Y%m%d%H%M%S')+'_Isweep')  
            
            plt.close(1)
            plt.figure(1)
            plt.plot(currents,voltages,'.k', label = 'Data')
            plt.ylabel('Voltage (V)')
            plt.xlabel('Current (mA)')    
            #plt.savefig(filename+'_IV.png')
            
            plt.close(2)
            plt.figure(2)
            plt.plot(currents,powers,'.k', label = 'Data')
            plt.ylabel('Power (dBm)')
            plt.xlabel('Current (mA)')    
            #plt.savefig(filename+'_LI.png')

            plt.close(3)
            plt.figure(3)
            plt.plot(currents,powersdbm,'.k', label = 'Data')
            plt.ylabel('Power (dBm)')
            plt.xlabel('Current (mA)')    
            #plt.savefig(filename+'_LI.png')

        pass



       
        