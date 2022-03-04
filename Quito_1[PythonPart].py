import serial
import time
import requests, urllib, webbrowser
import math

#ENTER your Id experience
idexperience="81"
#ENTER your secretkey
secretkey="228d"
things_key = "0RSUY8MLOJ80AXBJ" #ThingsSpeakAPi key
datastatus = "0" #Init of the status of the experience
#Trigger waterlevel:
level_end = 600
level_start = 10
# Temperature in & out
temperature_in = 20.0  
temperature_ext = 23.0
temperature_ice = 0.0
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


print("Start of the experience")

webbrowser.open_new("https://op-dev.icam.fr/~icebox/readExperience.php?idexperience="+ idexperience) 

def calculprediction(tempinside, tempice, tempoutside): #We add all sensors values to the calculation, but we decide to use only the ice and inside temperature
 # Ice  Reduction 
 IcubeSurfReduce = (IcubeHeight*(tempinside-tempice)*IcubeSurfInit*StarTime)/IcubeCI  
 IcubeVolReduce = (IcubeHeight*(tempinside-tempice)*IcubeVolInit*StarTime)/IcubeCI  

 IcubeSurface = ((IcubeHeight-IcubeSurfReduce)**2) 
 IcubeVolume = ((IcubeHeight-IcubeVolReduce)**3)  
 print("Volume :" + str(IcubeVolume))

 HeatRate = ((Boxk*BoxSurf)/BoxThickns)*(temperature_ext-temperature_in)  

 # h Convection Coeff Calculations
 h = (HeatRate)/(temperature_in-IcubeTempSurf)*IcubeSurface  

 # Melting time Calculations (Transient Conduction Formulas)
 t = (IcubeDensity*IcubeVolume*IcubeSpeHeat)/(h*IcubeSurface) 
 part1 = IcubeDensity*IcubeVolume*0.1*IcubeSpeHeat
 print("Density : " + str(IcubeDensity))
 print("Part1 :" + str(part1))
 print("Tho : " + str(t))
 print(math.log10((IcubeTempLiquid-temperature_in)/(IcubeTempSurf-temperature_in)))
 MeltingTime = (-1*t)*math.log10((IcubeTempLiquid-temperature_in)/(IcubeTempSurf-temperature_in))  
 print("Melting Time : " + str(MeltingTime))
 print("Melting time in min : " + str(MeltingTime/60)) 
 print("Melting time in hours : " + str(MeltingTime/3600))

 #Return the value calculated
 return MeltingTime

def substringBetween(textToSlice , start , end): #This function is used to isolate the variable in the serial port, is link to the way to print our values on the Arduino Code
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

def sendthingspeak(data_1, data_2, data_3, data_4, data_5): #This method send the sensors values to ThingSpeak API
 urlparameters1 = urllib.parse.urlencode({'api_key': things_key, 'field1' : data_1, 'field2' : data_2, 'field3' : data_3, 'field4' : data_4, 'field5' : data_5}) 
 print(urlparameters1)  #We print the url parameters to debug
 url1 = 'https://api.thingspeak.com/update?' + urlparameters1 
 resp = requests.get(url1)  #We send our URL and read the response 
 print(resp.text)
 print("Url ThingSpeank" + url1) 

def sendprediction(data): #This method send the prediction to Icam API
 urlparameters1 = urllib.parse.urlencode({ 'idexperience' :idexperience, 'prediction' : data, 'secretkey' : secretkey}) 
 print(urlparameters1)  #We print the url parameters to debug
 url1 = 'https://op-dev.icam.fr/~icebox/createPrediction.php?' + urlparameters1 
 resp = requests.get(url1)  #We send our URL and read the response
 print(resp.text)
 print("Url for prediction " + url1)

def sendstatus(data): #This method send the status of the experience to Icam API
 urlparameters2 = urllib.parse.urlencode({ 'idexperience' :idexperience, 'newStatus' : data, 'secretkey' : secretkey}) 
 print(urlparameters2)  #We print the url parameters to debug
 url2 = 'https://op-dev.icam.fr/~icebox/changeExperienceStatus.php?' + urlparameters2
 resp = requests.get(url2)  #We send our URL and read the response
 print(resp.text)
 print("Url for status " + url2)

while int(datastatus) < 2: #The code run until the end of the experience
 ser = serial.Serial('COM8', 9600, timeout=1)
 time.sleep(2)
 
 for i in range(10): # Read sensor on the serial port com
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
 
 prediction = calculprediction(temperature_in,temperature_ice,temperature_out)
 datastatus = findStatus(waterlevel) 
 
 sendstatus(int(datastatus)) #We send our status each min even if still the same value
 if (datastatus == 1 ): #We want to send a prediction only when the experience start
  sendthingspeak(temperature_ice,waterlevel,temperature_out,temperature_in,prediction)
  sendprediction(prediction)

 print("Prediction: " + str(prediction))
 print("Status: " + str(datastatus))
 
 time.sleep(60) #This delay is to avoid spamming the Icam API, which have a delay between two requests of 1 min
   
print("End of the experience")
webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
time.sleep(60) #We wait 60sec to be sure to be able to send the last status
sendstatus()

