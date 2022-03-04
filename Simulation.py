import matplotlib.pyplot as plt
import numpy as np
experianceDuration = 62 #Number of 1/2 hours in the experience

tn = np.full(experianceDuration,0.0)     #Creation of array
hours = np.full(experianceDuration,0.0)
temperature_in = np.full(experianceDuration,0.0)
temperature_ice = np.full(experianceDuration,0.0)
temperature_out = np.full(experianceDuration,0.0)

with open("SensorsIceBlock.txt") as file: #Buffer of lines readed in the log file
    lines = file.readlines()

print(lines)

for i in range(1,experianceDuration):    
 tn[i] = float(lines[i].split(";")[0]) 
 hours[i] = float(lines[i].split(";")[1])
 temperature_in[i] = float(lines[i].split(";")[2])
 temperature_out[i] = float(lines[i].split(";")[3])
 temperature_ice[i] =  float(lines[i].split(";")[4])
 print("Tn : "+ str(tn[i]) + " Hours : " + str(hours[i]) + " Temp in =" + str(temperature_in[i]) + " Temp out : " + str(temperature_out[i]) + " Temp ice : " + str(temperature_ice[i]))


plt.plot(tn, temperature_in, label = "Temperature Inside")
plt.plot(tn, temperature_out, label = "Temperature Outside")
plt.plot(tn, temperature_ice, label = "Temperature Ice")
plt.legend() 
plt.show()