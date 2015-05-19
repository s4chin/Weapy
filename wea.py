import requests
import ConfigParser
import argparse
import datetime

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
        
        def parse_response(self, response, current=None):
            if not current:
                daily_weather = response['data']['weather']
                for daily in daily_weather:
                    if daily['date'] == self.date:
                        hourly_weather = daily['hourly']
                        for hourly in hourly_weather:
                            if hourly['time'] == self.time:
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
                self.winddir16Point = hourly['winddir16Point']
                self.weatherDesc = hourly['weatherDesc'][0]['value']
                self.windspeedKmph = hourly['windspeedKmph']
                self.visibility = hourly['visibility']
                self.humidity = hourly['humidity']
                self.precipMM = hourly['precipMM']
                self.windspeedMiles = hourly['windspeedMiles']
                self.tempC = hourly['temp_C']
                self.FeelsLikeC = hourly['FeelsLikeC']


def display_day(day, current):
    display_hour(current)
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

def format_op(day):
    pass

current = Day.Time('0000', '0000')
current.parse_response(response=response, current=True)
for i in range(num_of_days):
    date_of_day = datetime.date.today() + datetime.timedelta(days=i)
    d_string = date_of_day.strftime('%Y-%m-%d')
    day = Day(d_string)
    day.parse_response(response)
    display_day(day, current)
