import requests
import ConfigParser
import argparse
import datetime
import sys

key = 'key'
q = 'Mumbai'
num_of_days = 3

url = 'http://api.worldweatheronline.com/free/v2/weather.ashx?q=%s&format=json&num_of_days=%d&key=%s' \
      % (q, num_of_days, key)

r = requests.get(url)
response = r.json()

def parse_place(response):
    place = response['data']['request'][0]
    name_of_place = place['query']
    type_of_place = place['type']

class Day:
    def __init__(self, date):
        self.date = date
        self.morn = self.Time(time='830', date=date)
        self.aftn = self.Time(time='1130', date=date)
        self.even = self.Time(time='2030', date=date)
        self.nigh = self.Time(time='2330', date=date)
    
    def parse_response(self, response):
        self.morn.parse_response(response)
        self.aftn.parse_response(response)
        self.even.parse_response(response)
        self.nigh.parse_response(response)
            
    class Time:
        def __init__(self, date, time):
            self.date = date
            self.time = time
        
        def parse_response(self, response, current_hour=None):
            if not current_hour:
                daily_weather = response['data']['weather']
                for daily in daily_weather:
                    if daily['date'] == self.date:
                        hourly_weather = daily['hourly']
                        for hourly in hourly_weather:
                            if hourly['time'] == self.time:
                                self.weatherCode = hourly['weatherCode']
                                self.winddir16Point = hourly['winddir16Point']
                                self.weatherDesc = hourly['weatherDesc'][0]['value']
                                self.windspeedKmph = hourly['windspeedKmph']
                                self.chanceofrain = hourly['chanceofrain']
                                self.visibility = hourly['visibility']
                                self.humidity = hourly['humidity']
                                self.precipMM = hourly['precipMM']
                                self.WindGustMiles = hourly['WindGustMiles']
                                self.WindGustKmph = hourly['WindGustKmph']
                                self.windspeedMiles = hourly['windspeedMiles']
                                self.tempC = hourly['tempC']
                                self.FeelsLikeC = hourly['FeelsLikeC']
            else:
                hourly = response['data']['current_condition'][0]
                self.weatherCode = hourly['weatherCode']
                self.winddir16Point = hourly['winddir16Point']
                self.weatherDesc = hourly['weatherDesc'][0]['value']
                self.windspeedKmph = hourly['windspeedKmph']
                self.visibility = hourly['visibility']
                self.humidity = hourly['humidity']
                self.precipMM = hourly['precipMM']
                self.windspeedMiles = hourly['windspeedMiles']
                self.tempC = hourly['temp_C']
                self.FeelsLikeC = hourly['FeelsLikeC']


def display_day(day, current_hour):
    display_hour(current_hour)
    display_hour(day.morn)
    display_hour(day.aftn)
    display_hour(day.even)
    display_hour(day.nigh)

def display_hour(hour):
    print hour.date
    print hour.time
    print hour.weatherDesc
    print hour.tempC
    print hour.winddir16Point
    print hour.humidity

def format_op(hour):
    pass

current_hour = Day.Time('0000', '0000')
current_hour.parse_response(response=response, current_hour=True)
for i in range(num_of_days):
    date_of_day = datetime.date.today() + datetime.timedelta(days=i)
    d_string = date_of_day.strftime('%Y-%m-%d')
    day = Day(d_string)
    day.parse_response(response)
    display_day(day, current_hour)

##############################################################################

iconUnknown = [
    "    .-.      ",
    "     __)     ",
    "    (        ",
    "     `-’     ",
    "      •      "]
iconSunny = [
    "\033[38;5;226m    \\   /    \033[0m",
    "\033[38;5;226m     .-.     \033[0m",
    "\033[38;5;226m  ― (   ) ―  \033[0m",
    "\033[38;5;226m     `-’     \033[0m",
    "\033[38;5;226m    /   \\    \033[0m"]
iconPartlyCloudy = [
    "\033[38;5;226m   \\  /\033[0m      ",
    "\033[38;5;226m _ /\"\"\033[38;5;250m.-.    \033[0m",
    "\033[38;5;226m   \\_\033[38;5;250m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
    "             "]
iconCloudy = [
    "             ",
    "\033[38;5;250m     .--.    \033[0m",
    "\033[38;5;250m  .-(    ).  \033[0m",
    "\033[38;5;250m (___.__)__) \033[0m",
    "             "]
iconVeryCloudy = [
    "             ",
    "\033[38;5;240;1m     .--.    \033[0m",
    "\033[38;5;240;1m  .-(    ).  \033[0m",
    "\033[38;5;240;1m (___.__)__) \033[0m",
    "             "]
iconLightShowers = [
    "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
    "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
    "\033[38;5;111m     ‘ ‘ ‘ ‘ \033[0m",
    "\033[38;5;111m    ‘ ‘ ‘ ‘  \033[0m"]
iconHeavyShowers = [
    "\033[38;5;226m _`/\"\"\033[38;5;240;1m.-.    \033[0m",
    "\033[38;5;226m  ,\\_\033[38;5;240;1m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;240;1m(___(__) \033[0m",
    "\033[38;5;21;1m   ‚‘‚‘‚‘‚‘  \033[0m",
    "\033[38;5;21;1m   ‚’‚’‚’‚’  \033[0m"]
iconLightSnowShowers = [
    "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
    "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
    "\033[38;5;255m     *  *  * \033[0m",
    "\033[38;5;255m    *  *  *  \033[0m"]
iconHeavySnowShowers = [
    "\033[38;5;226m _`/\"\"\033[38;5;240;1m.-.    \033[0m",
    "\033[38;5;226m  ,\\_\033[38;5;240;1m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;240;1m(___(__) \033[0m",
    "\033[38;5;255;1m    * * * *  \033[0m",
    "\033[38;5;255;1m   * * * *   \033[0m"]
iconLightSleetShowers = [
    "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
    "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
    "\033[38;5;111m     ‘ \033[38;5;255m*\033[38;5;111m ‘ \033[38;5;255m* \033[0m",
    "\033[38;5;255m    *\033[38;5;111m ‘ \033[38;5;255m*\033[38;5;111m ‘  \033[0m"]
iconThunderyShowers = [
    "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
    "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
    "\033[38;5;228;5m    ⚡\033[38;5;111;25m‘ ‘\033[38;5;228;5m⚡\033[38;5;111;25m‘ ‘ \033[0m",
    "\033[38;5;111m    ‘ ‘ ‘ ‘  \033[0m"]
iconThunderyHeavyRain = [
    "\033[38;5;240;1m     .-.     \033[0m",
    "\033[38;5;240;1m    (   ).   \033[0m",
    "\033[38;5;240;1m   (___(__)  \033[0m",
    "\033[38;5;21;1m  ‚‘\033[38;5;228;5m⚡\033[38;5;21;25m‘‚\033[38;5;228;5m⚡\033[38;5;21;25m‚‘   \033[0m",
    "\033[38;5;21;1m  ‚’‚’\033[38;5;228;5m⚡\033[38;5;21;25m’‚’   \033[0m"]
iconThunderySnowShowers = [
    "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
    "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
    "\033[38;5;255m     *\033[38;5;228;5m⚡\033[38;5;255;25m *\033[38;5;228;5m⚡\033[38;5;255;25m * \033[0m",
    "\033[38;5;255m    *  *  *  \033[0m"]
iconLightRain = [
    "\033[38;5;250m     .-.     \033[0m",
    "\033[38;5;250m    (   ).   \033[0m",
    "\033[38;5;250m   (___(__)  \033[0m",
    "\033[38;5;111m    ‘ ‘ ‘ ‘  \033[0m",
    "\033[38;5;111m   ‘ ‘ ‘ ‘   \033[0m"]
iconHeavyRain = [
    "\033[38;5;240;1m     .-.     \033[0m",
    "\033[38;5;240;1m    (   ).   \033[0m",
    "\033[38;5;240;1m   (___(__)  \033[0m",
    "\033[38;5;21;1m  ‚‘‚‘‚‘‚‘   \033[0m",
    "\033[38;5;21;1m  ‚’‚’‚’‚’   \033[0m"]
iconLightSnow = [
    "\033[38;5;250m     .-.     \033[0m",
    "\033[38;5;250m    (   ).   \033[0m",
    "\033[38;5;250m   (___(__)  \033[0m",
    "\033[38;5;255m    *  *  *  \033[0m",
    "\033[38;5;255m   *  *  *   \033[0m"]
iconHeavySnow = [
    "\033[38;5;240;1m     .-.     \033[0m",
    "\033[38;5;240;1m    (   ).   \033[0m",
    "\033[38;5;240;1m   (___(__)  \033[0m",
    "\033[38;5;255;1m   * * * *   \033[0m",
    "\033[38;5;255;1m  * * * *    \033[0m"]
iconLightSleet = [
    "\033[38;5;250m     .-.     \033[0m",
    "\033[38;5;250m    (   ).   \033[0m",
    "\033[38;5;250m   (___(__)  \033[0m",
    "\033[38;5;111m    ‘ \033[38;5;255m*\033[38;5;111m ‘ \033[38;5;255m*  \033[0m",
    "\033[38;5;255m   *\033[38;5;111m ‘ \033[38;5;255m*\033[38;5;111m ‘   \033[0m"]
iconFog = [
    "             ",
    "\033[38;5;251m _ - _ - _ - \033[0m",
    "\033[38;5;251m  _ - _ - _  \033[0m",
    "\033[38;5;251m _ - _ - _ - \033[0m",
    "             "]

weatherCodes = {
    '113': iconSunny,
    '116': iconPartlyCloudy,
    '119': iconCloudy,
    '122': iconVeryCloudy,
    '143': iconFog,
    '176': iconLightShowers,
    '179': iconLightSleetShowers,
    '182': iconLightSleet,
    '185': iconLightSleet,
    '200': iconThunderyShowers,
    '227': iconLightSnow,
    '230': iconHeavySnow,
    '248': iconFog,
    '260': iconFog,
    '263': iconLightShowers,
    '266': iconLightRain,
    '281': iconLightSleet,
    '284': iconLightSleet,
    '293': iconLightRain,
    '296': iconLightRain,
    '299': iconHeavyShowers,
    '302': iconHeavyRain,
    '305': iconHeavyShowers,
    '308': iconHeavyRain,
    '311': iconLightSleet,
    '314': iconLightSleet,
    '317': iconLightSleet,
    '320': iconLightSnow,
    '323': iconLightSnowShowers,
    '326': iconLightSnowShowers,
    '329': iconHeavySnow,
    '332': iconHeavySnow,
    '335': iconHeavySnowShowers,
    '338': iconHeavySnow,
    '350': iconLightSleet,
    '353': iconLightShowers,
    '356': iconHeavyShowers,
    '359': iconHeavyRain,
    '362': iconLightSleetShowers,
    '365': iconLightSleetShowers,
    '368': iconLightSnowShowers,
    '371': iconHeavySnowShowers,
    '374': iconLightSleetShowers,
    '377': iconLightSleet,
    '386': iconThunderyShowers,
    '389': iconThunderyHeavyRain,
    '392': iconThunderySnowShowers,
    '395': iconHeavySnowShowers, # ThunderyHeavySnow
    }


for line in weatherCodes['143']:
    print line
