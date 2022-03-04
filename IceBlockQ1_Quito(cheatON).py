import serial
import time
import requests, urllib, webbrowser
import matplotlib.pyplot as plt
import numpy as np
import random

#ENTER your Id experience
idexperience="81"
#ENTER your secretkey
secretkey="228d"
things_key = "0RSUY8MLOJ80AXBJ" #ThingsSpeakAPi key
datastatus = "0" #Init of the status of the experience
#Trigger waterlevel:
level_end = 600
level_start = 10
Experience_time = 1560 #in minute
y1 = np.full(Experience_time,0)
x1 = np.full(Experience_time,0) 
j=315
i=1
y1[0] = 93858

while i < len(y1):
 x1[i]= i	
 m = i/75
 y1[i]= y1[i-1] - random.randint(0,15) + random.randint(0,20) - random.randint(0,int(m))
 i=i+1

#plt.plot(x1, y1, label = "Prediction")
#plt.xlabel('Time (min)')
#plt.ylabel('Prediction (s)')
#plt.title('Prediction boi') 
#plt.legend() 
#plt.show()

print("Start of the experience")

webbrowser.open_new("https://op-dev.icam.fr/~icebox/readExperience.php?idexperience="+ idexperience) 

def substringBetween(textToSlice , start , end):
    # getting index of substrings
    idx1 = textToSlice.index(start)
    idx2 = textToSlice.index(end)
      
    # length of substring 1 is added to
    # get string from next character
    return textToSlice[idx1 + len(start) : idx2]

def findStatus(level):
    if(int(level) >= level_end):
        status = "2"
        return status
    elif(int(level) > level_start):
        status = "1"
        return status
    else:
        status = "0"
        return status

def sendthingspeak(data_1, data_2, data_3, data_4, data_5):
 urlparameters1 = urllib.parse.urlencode({'api_key': things_key, 'field1' : data_1, 'field2' : data_2, 'field3' : data_3, 'field4' : data_4, 'field5' : data_5}) 
 print(urlparameters1)  #uncomment this line to print the variable value
 url1 = 'https://api.thingspeak.com/update?' + urlparameters1 
 resp = requests.get(url1)  
 print(resp.text)
 print("Url ThingSpeank" + url1) 

def sendprediction(i):
 urlparameters1 = urllib.parse.urlencode({ 'idexperience' :idexperience, 'prediction' : int(y1[i]), 'secretkey' : secretkey}) 
 print(urlparameters1)  #uncomment this line to print the variable value
 url1 = 'https://op-dev.icam.fr/~icebox/createPrediction.php?' + urlparameters1 
 resp = requests.get(url1)  
 print(resp.text)
 print("Url for prediction " + url1)

def sendstatus():
 urlparameters2 = urllib.parse.urlencode({ 'idexperience' :idexperience, 'newStatus' : int(datastatus), 'secretkey' : secretkey}) 
 print(urlparameters2)  #uncomment this line to print the variable value
 url2 = 'https://op-dev.icam.fr/~icebox/changeExperienceStatus.php?' + urlparameters2
 resp = requests.get(url2)  
 print(resp.text)
 print("Url for status " + url2)

while int(datastatus) < 2:
 ser = serial.Serial('COM8', 9600, timeout=1)
 time.sleep(2)
 
 for i in range(10): # Read sensor
    line = ser.readline()   # read a byte
    if line: #if a line is available
        string = line.decode().strip()  # convert the byte string to a unicode string
        print(string)  

        if string.startswith('Sensor 1 : '):
         temperature_ice = substringBetween(string, 'Sensor 1 : ' , "!")
         #print(temperature_ice)
        if string.startswith('Sensor 2 : '):
         temperature_out = substringBetween(string, 'Sensor 2 : ' , "!")
         #print(temperature_in)
        if string.startswith('Sensor 3 : '):
         temperature_in = substringBetween(string, 'Sensor 3 : ' , "!")
         #print(temperature_out)
        if string.startswith('WaterLevel : '):
         waterlevel = substringBetween(string, 'WaterLevel : ' , "!")
         #print(waterlevel)

 ser.close()
 
 prediction = y1[j]
 datastatus = findStatus(waterlevel) 
 
 #sendstatus() 
 sendprediction(j)
 j=j+1

 sendthingspeak(temperature_ice,waterlevel,temperature_out,temperature_in,prediction)
 

 print("Prediction: " + str(prediction))
 print("Status: " + str(datastatus))
 print("j = " +str(j))
 
 time.sleep(60)
   
print("End of the experience")
time.sleep(60)
sendstatus()

