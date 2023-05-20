from datetime import date
from pushbullet import Pushbullet
import requests, json
import time


#token patrick
pb = Pushbullet("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
#set device samsung patrick
dev = pb.get_device("Samsung SM-A528B")

#get weather from openweather
base_url = "https://api.openweathermap.org/data/2.5/forecast?"
city = "Bern"
api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

#set proper url
url = base_url + "q=" + city + "&appid=" + api_key
#http request
response = requests.get(url)


#thermometer function - up to roughly 35 * | if fits in one line of the pushbullet notification
def thermometer(temp_kelvin):
    #calc weather from kelvin to celsius
    temp_celsius = round(temp_kelvin - 273.15)

    #create thermometer ascii
    if temp_celsius > 0:
        thermometer_chars = "|" * int(temp_celsius)
        thermometer = thermometer_chars + str(temp_celsius) + "°"
        return thermometer
    
    else:
        thermometer_chars = "-" * abs(int(temp_celsius) + 1) #correction for when temp is negative
        thermometer = thermometer_chars + str(temp_celsius) + "°"   
        return thermometer    


#weather icon assignment function - id source https://openweathermap.org/weather-conditions
def weather_icon(id):

    #weather icons
    weather_icons = ["☀️","☁️","☔","❄️","⛅","🌦️","🌩️"]

    #create message with icon based on weather id
    if 200 <= id <= 232:
        return weather_icons[6] + " - Thunderstorm"
    
    elif 600 <= id <= 622:
        return weather_icons[3] + " - Snow"
    
    elif id == 800:
        return weather_icons[0] + " - Clear Sky"
    
    elif 801 <= id <= 802:
        return weather_icons[4] + " - Few Clouds"
    
    elif 803 <= id <= 804:
        return weather_icons[1] + " - Cloudy, Overcast"
    
    elif id == 500 or 300 <= id <= 301:
        return weather_icons[5] + " - Slight Rain, Drizzle"
    
    elif 302 <= id <= 321 or 501 <= id <= 531:
        return weather_icons[2] + " - Rain"

def wind_desc(speed):

    #round to one decimal, easier to compare to wind speed metrics
    speed = round(speed, 1)

    #create message based on wind speeds
    if speed < 0.5:
        return f"Almost no wind - {speed} m/s"
    elif 0.5 <= speed <= 3.3:
        return f"Light breeze - {speed} m/s"
    elif 3.4 <= speed <= 5.4:
        return f"Gentle breeze - {speed} m/s"
    elif 5.5 <= speed <= 7.9:
        return f"Moderate breeze - {speed} m/s"
    elif 8.0 <= speed <= 10.7:
        return f"It's getting windy - {speed} m/s"
    elif 10.8 <= speed <= 13.8:
        return f"IT'S FUCKING WINDYYY - {speed} m/s"
    else:
        return f"JESUS FUCK ITS WINDY - {speed} m/s" 



#if response is there, get the data
if response.status_code == 200:

    #get data in json
    data = response.json()

    #date
    today = date.today()


    #data collection


    #temp
    six = data['list'][0]['main']['temp']
    nine = data['list'][1]['main']['temp']
    twelve = data['list'][2]['main']['temp']
    fifteen = data['list'][3]['main']['temp']
    eighteen = data['list'][4]['main']['temp']
    twentyone = data['list'][5]['main']['temp']
    midnight = data['list'][6]['main']['temp']
    three = data['list'][7]['main']['temp']

    #weather state
    six_weather = data['list'][0]['weather'][0]['id']
    nine_weather = data['list'][1]['weather'][0]['id']
    twelve_weather = data['list'][2]['weather'][0]['id']
    fifteen_weather = data['list'][3]['weather'][0]['id']
    eighteen_weather = data['list'][4]['weather'][0]['id']
    twentyone_weather = data['list'][5]['weather'][0]['id']
    midnight_weather = data['list'][6]['weather'][0]['id']
    three_weather = data['list'][6]['weather'][0]['id']

    #wind speeds
    six_wind = data['list'][0]['wind']['speed']
    nine_wind = data['list'][1]['wind']['speed']
    twelve_wind = data['list'][2]['wind']['speed']
    fifteen_wind = data['list'][3]['wind']['speed']
    eighteen_wind = data['list'][4]['wind']['speed']
    twentyone_wind = data['list'][5]['wind']['speed']
    midnight_wind = data['list'][6]['wind']['speed']
    three_wind = data['list'][6]['wind']['speed']



    #data preparation


    #thermometer values temp
    six_T = thermometer(six)
    nine_T = thermometer(nine)
    twelve_T = thermometer(twelve)
    fifteen_T = thermometer(fifteen)
    eighteen_T = thermometer(eighteen)
    twentyone_T = thermometer(twentyone)
    midnight_T = thermometer(midnight)
    three_T = thermometer(three)

    #weather icons
    six_ic = weather_icon(six_weather)
    nine_ic = weather_icon(nine_weather)
    twelve_ic = weather_icon(twelve_weather)
    fifteen_ic = weather_icon(fifteen_weather)
    eighteen_ic = weather_icon(eighteen_weather)
    twentyone_ic = weather_icon(twentyone_weather)
    midnight_ic = weather_icon(midnight_weather)
    three_ic = weather_icon(three_weather)

    #wind message
    six_w = wind_desc(six_wind)
    nine_w = wind_desc(nine_wind)
    twelve_w = wind_desc(twelve_wind)
    fifteen_w = wind_desc(fifteen_wind)
    eighteen_w = wind_desc(eighteen_wind)
    twentyone_w = wind_desc(twentyone_wind)
    midnight_w = wind_desc(midnight_wind)
    three_w = wind_desc(three_wind)


    #final message
    message = f'''
Temperature:
06 {six_T}
09 {nine_T}
12 {twelve_T}
15 {fifteen_T}
18 {eighteen_T}
21 {twentyone_T}
00 {midnight_T}
03 {three_T}

Weather: 
06 {six_ic}
09 {nine_ic}
12 {twelve_ic}
15 {fifteen_ic}
18 {eighteen_ic}
21 {twentyone_ic}
00 {midnight_ic}
03 {three_ic}

Wind:
06 {six_w}
09 {nine_w}
12 {twelve_w}
15 {fifteen_w}
18 {eighteen_w}
21 {twentyone_w}
00 {midnight_w}
03 {three_w}
        '''

    #message push
    push = dev.push_note(f"Weather for {today}:", message)
