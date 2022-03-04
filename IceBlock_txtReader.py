import requests, urllib, webbrowser
import time

with open("IceBlock.txt") as file: #Buffer of lines readed in the log file
    lines = file.readlines()

#Id experience
idexperience="31"
#enter your secretkey
secretkey="daee"

def sendprediction():
 urlparameters1 = urllib.parse.urlencode({ 'idexperience' :idexperience, 'prediction' : int(prediction), 'secretkey' : secretkey}) 
 print(urlparameters1)  #uncomment this line to print the variable value
 url1 = 'https://op-dev.icam.fr/~icebox/createPrediction.php?' + urlparameters1
 print(url1)
 resp = requests.get(url1)
 print(resp.status_code)  
 print(resp.text)

def sendstatus():
 urlparameters2 = urllib.parse.urlencode({ 'idexperience' :idexperience, 'newStatus' : status, 'secretkey' : secretkey}) 
 print(urlparameters2)  #uncomment this line to print the variable value
 url2 = 'https://op-dev.icam.fr/~icebox/changeExperienceStatus.php?' + urlparameters2
 print(url2)
 resp = requests.get(url2)
 print(resp.status_code)  
 print(resp.text)

for i in range(len(lines)):
 status= lines[i].split(",")[0]  
 prediction = lines[i].split(",")[1]
 sendprediction()
 sendstatus()   
 print(status)  
 print(prediction)
 time.sleep(60)   
 


