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

class Day:
    def __init__(self, date):
        if date != 'current':
            self.date = date
            self.morn = self.Time(time='0830', date=date)
            self.aftn = self.Time(time='1130', date=date)
            self.even = self.Time(time='0830', date=date)
            self.nigh = self.Time(time='1130', date=date)
        else:
            self.date = date
            self.current = self.Time(time='0000', date = date)
    def parse_response(self):
        if self.date != 'current'
            self.morn.parse_response()
            self.aftn.parse_response()
            self.even.parse_response()
            self.nigh.parse_response()
            
    class Time:
        def __init__(self, date, time):
            self.date = date
            self.time = time
        def parse_response(self):
            self.winddir16Point = 34
            self.weatherDesc = 34
            self.windspeedKmph = 34
            self.chanceofrain = 34
            self.visibility = 34
            self.humidity = 34
            self.precipMM = 34
            self.chanceofrain = 34
            self.WindGustKmph = 34
            self.winddir16Point = 34
            self.tempC = 34
            self.FeelsLikeC = 34

def display(day):
    print day.aftn.date

def format_op(day):
    pass

for i in range(num_of_days):
    date_of_day = datetime.date.today() + datetime.timedelta(days=i)
    day = Day('%d-%d-%d' % (date_of_day.year, date_of_day.month, date_of_day.day))
    day.parse_response()
    display(day)
