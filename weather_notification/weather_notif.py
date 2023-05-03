from datetime import date
from pushbullet import Pushbullet
import requests, json
import time


#token
pb = Pushbullet("o.1WBLdaCPq6RO6Ax0LZV7yHAd3gguE5m7")
#set device
dev = pb.get_device("Samsung SM-A528B")

#get weather from opernweather
base_url = "https://api.openweathermap.org/data/2.5/forecast?"
city = "Bern"
api_key = "5d1843bc8fba39e9d4a05ca0d6213991"

#set proper url
url = base_url + "q=" + city + "&appid=" + api_key
#http request
response = requests.get(url)

#if response is there, get the data
if response.status_code == 200:

        #get data in json
        data = response.json()

        #stats for 6am
    
        #tmin
        amtmin = data['list'][0]['main']['temp_min']
        amtmin = round(amtmin - 273.15)

        #tmax
        amtmax = data['list'][0]['main']['temp_max']
        amtmax = round(amtmax - 273.15)   

        #wind
        amwind = data['list'][0]['wind']['speed']

        #state
        amstate = data['list'][0]['weather'][0]['description']

        #stats for 3pm

        #tmin
        pmtmin = data['list'][3]['main']['temp_min']
        pmtmin = round(pmtmin - 273.15)

        #tmax
        pmtmax = data['list'][3]['main']['temp_max']
        pmtmax = round(pmtmax - 273.15)   

        #wind
        pmwind = data['list'][3]['wind']['speed']

        #state
        pmstate = data['list'][3]['weather'][0]['description']


        #date
        today = date.today()

        #message
        message = f'''
Weather for today in Bern:

Weather:
{amstate} - {pmstate} 

AM Temperature: 
{amtmin}° - {amtmax}° 

PM Temperature: 
{pmtmin}° - {pmtmax}°

Windy? 
Morning ({amwind}) vs. evening ({pmwind})
        '''

        print(message)
        push = dev.push_note(f"Weather for {today}:", message)
else:
        push = dev.push_note("Error", "The API request made a fucky wucky, oopsie")
