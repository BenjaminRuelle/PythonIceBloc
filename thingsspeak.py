import requests, urllib, webbrowser
import random

things_key = "0RSUY8MLOJ80AXBJ"
temperature_in = random.randint(13,15)
temperature_ice = random.randint(0,6)
temperature_out = random.randint(18,25)
waterlevel= random.randint(0,650)

def sendthingspeak(data_1, data_2, data_3, data_4):
 urlparameters1 = urllib.parse.urlencode({'api_key': things_key, 'field1' : data_1, 'field2' : data_2, 'field3' : data_3, 'field4' : data_4}) 
 print(urlparameters1)  #uncomment this line to print the variable value
 url1 = 'https://api.thingspeak.com/update?' + urlparameters1 
 resp = requests.get(url1)  
 print(resp.text)
 print("Url for prediction " + url1)  

while 1>0:
 temperature_in = random.randint(13,15)
 temperature_ice = random.randint(0,6)
 temperature_out = random.randint(18,25)
 waterlevel= random.randint(0,650)
 sendthingspeak(temperature_ice,waterlevel,temperature_out,temperature_in)
 print("Temperature in : " + str(temperature_in))
 print("Temperature out : " + str(temperature_out))
 print("Temperature ice : " + str(temperature_ice))
 print("Water level : " + str(waterlevel))