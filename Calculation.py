
import matplotlib.pyplot as plt
import numpy as np
import random
x1 = np.full(1260,0)
y1 = np.full(1260,0)
i=3

Experience_time = 1560 #in minute
y1 = np.full(Experience_time,0)
x1 = np.full(Experience_time,0) 
j=0
i=1
y1[0] = 93655
while i < len(y1):
 x1[i]= i	
 m = i/75
 y1[i]= y1[i-1] - random.randint(0,15) + random.randint(0,20) - random.randint(0,int(m))
 i=i+1

print(y1)
plt.plot(x1, y1, label = "Prediction") 
# naming the x axis
plt.xlabel('Time (min)')
# naming the y axis
plt.ylabel('Prediction (s)')
# giving a title to my graph
plt.title('Prediction boi') 
# show a legend on the plot
plt.legend() 
# function to show the plot
plt.show()