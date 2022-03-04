import matplotlib.pyplot as plt
import numpy as np
from numpy import trapz

experienceDuration_Hours =  31 
experienceTick = experienceDuration_Hours*2  #We want to have a frequency of 30min

tn = np.full(experienceTick,0.0)     #Creation of arrays
hours = np.full(experienceTick,0.0)
temperature_in = np.full(experienceTick,0.0)
temperature_ice = np.full(experienceTick,0.0)
temperature_out = np.full(experienceTick,0.0)
prediction = np.full(experienceTick,0.0)


#Calculation variables
# Time
StarTime = 100.0
# Ice Cube Data
IcubeNbFaces = 6.0  
IcubeLength = 0.1  
IcubeHeight = 0.1  
IcubeWidth = 0.1
IcubeCI = 334.0 
IcubeSpeHeat = 2090.0  
IcubeDensity = 925.0
IcubeTempSurf = 0.0 
IcubeTempLiquid = 0.5
#Initial state
IcubeSurfInit = IcubeHeight*IcubeLength*6  
IcubeVolInit = IcubeHeight*IcubeWidth*IcubeLength
# Styrofoam Box Data
BoxLength = 0.265  
BoxHeight = 0.25  
BoxThickns = 0.02
BoxSurf = BoxHeight*BoxLength
Boxk = 0.0263  

def calculprediction(tempinside, tempice, tempoutside): #We add all sensors values to the calculation, but we decide to use only the ice and inside temperature
 # Ice  Reduction  
 IcubeSurfReduce = (IcubeHeight*(tempinside-tempice)*IcubeSurfInit*StarTime)/IcubeCI  
 IcubeVolReduce = (IcubeHeight*(tempinside-tempice)*IcubeVolInit*StarTime)/IcubeCI  

 IcubeSurface = ((IcubeHeight-IcubeSurfReduce)**2)
 IcubeVolume = ((IcubeHeight-IcubeVolReduce)**2)  
 #print("Volume :" + str(IcubeVolume))

 HeatRate = ((Boxk*BoxSurf)/BoxThickns)*(tempoutside-tempinside)  

 # h Convection Coeff Calculations
 h = (HeatRate)/((tempinside-tempice)*IcubeSurface)

 # Melting time Calculations (Transient Conduction Formulas)
 t = (IcubeDensity*IcubeVolume*IcubeSpeHeat)/(h*IcubeSurface) 
 part1 = IcubeDensity*IcubeVolume*IcubeSpeHeat
 #print("Density : " + str(IcubeDensity))
 #print("Part1 :" + str(part1))
 #print("Tho : " + str(t))
 ln = 8*np.log((IcubeTempLiquid-tempinside)/(IcubeTempSurf-tempinside))
 #print("Log10(x): " + str(log10x))

 MeltingTime = ((-1*t)*ln)*1.7
 MeltingTime_Hours = MeltingTime/3600
 #print("Melting Time : " + str(MeltingTime))
 #print("Melting time in min : " + str(MeltingTime/60)) 
 #print("Melting time in hours : " + str(MeltingTime/3600))

 return MeltingTime_Hours

with open("SensorsIceBlock.txt") as file: #Buffer of lines readed in the log file
    lines = file.readlines()

for i in range(1,experienceTick):

 tn[i] = float(lines[i].split(";")[0]) 
 hours[i] = float(lines[i].split(";")[1])
 temperature_in[i] = float(lines[i].split(";")[2])
 temperature_out[i] = float(lines[i].split(";")[3])
 temperature_ice[i] =  float(lines[i].split(";")[4])

 print("Tn : "+ str(tn[i]) + " Hours : " + str(hours[i]) + " Temperature in =" + str(temperature_in[i]) + " Temperature out : " + str(temperature_out[i]) + " Temperature ice : " + str(temperature_ice[i]))
 
 prediction[i] = calculprediction(temperature_in[i], temperature_ice[i],temperature_out[i])
 print("Prediction : "  + str(prediction[i]) + " hours")

score = np.trapz(prediction, x = None, dx = experienceDuration_Hours, axis = -1)
print("Nice job ! Your score is: " + str(score))

plt.plot(tn, temperature_in, label = "Temperature Inside")
plt.plot(tn, temperature_out, label = "Temperature Outside")
plt.plot(tn, temperature_ice, label = "Temperature Ice")
plt.plot(tn, prediction, label = "Prediction (hours)")
plt.legend() 
plt.show()

