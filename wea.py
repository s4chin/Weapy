# -*- coding: utf-8 -*-
# encoding=utf8
import requests
import ConfigParser
import argparse
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf8') # As per http://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte
sys.version = '2.7.3 (default, Apr 12 2012, 14:30:37) [MSC v.1500 32 bit (Intel)]' # As per http://stackoverflow.com/questions/19105255/praw-failed-to-parse-cpython-sys-version-when-creating-reddit-object

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

windDir = {
    "N":   "\033[1m↓\033[0m",
    "NNE": "\033[1m↓\033[0m",
    "NE":  "\033[1m↙\033[0m",
    "ENE": "\033[1m↙\033[0m",
    "E":   "\033[1m←\033[0m",
    "ESE": "\033[1m←\033[0m",
    "SE":  "\033[1m↖\033[0m",
    "SSE": "\033[1m↖\033[0m",
    "S":   "\033[1m↑\033[0m",
    "SSW": "\033[1m↑\033[0m",
    "SW":  "\033[1m↗\033[0m",
    "WSW": "\033[1m↗\033[0m",
    "W":   "\033[1m→\033[0m",
    "WNW": "\033[1m→\033[0m",
    "NW":  "\033[1m↘\033[0m",
    "NNW": "\033[1m↘\033[0m",
}

key = 'key'

url = ''

response = ''

def parse_place(response):
    place = response['data']['request'][0]
    name_of_place = place['query']
    type_of_place = place['type']
    sys.stdout.write(name_of_place + " " + type_of_place + "\n\n")

class Day:
    def __init__(self, date):
        self.date = date
        self.morn = self.Time(time='830', date=date)
        self.aftn = self.Time(time='1130', date=date)
        self.even = self.Time(time='1730', date=date)
        self.nigh = self.Time(time='2030', date=date)

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
                            if int(hourly['time'])-int(self.time) <= 170 and int(hourly['time'])-int(self.time) > -130:
                                #print int(hourly['time']), int(self.time)
                                self.weatherCode = hourly['weatherCode']
                                #print self.weatherCode
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

def format_hour(hour, current=None):
    icon = list(weatherCodes[hour.weatherCode])
    icon[0] += (hour.weatherDesc).ljust(17)[:17]
    if hour.FeelsLikeC > hour.tempC:
        icon[1] += (color_temp(hour.tempC) + "-" + color_temp(hour.FeelsLikeC) + "C").ljust(17)
    else:
        icon[1] += (color_temp(hour.FeelsLikeC) + "-" + color_temp(hour.tempC) + "C").ljust(17)
    icon[2] += windDir[hour.winddir16Point] + " "
    if not current:
        if hour.WindGustKmph > hour.windspeedKmph:
            icon[2] += (color_windspeed(hour.windspeedKmph) + "-" + color_windspeed(hour.WindGustKmph) + "km/h").ljust(15)
        else:
            icon[2] += (color_windspeed(hour.WindGustKmph) + "-" + color_windspeed(hour.windspeedKmph) + "km/h").ljust(15)
    else:
        icon[2] += (color_windspeed(hour.windspeedKmph) + "km/h").ljust(15)
    icon[3] += (hour.visibility + "km").ljust(17)
    if not current:
        icon[4] +=  (hour.precipMM + "mm" + "|" + hour.chanceofrain + "%").ljust(17)
    else:
        icon[4] += hour.precipMM + "mm"
        icon[4] = (icon[4]).ljust(17)
    return icon


def color_temp(temp):
    return temp

def color_windspeed(windspeed):
    return windspeed

def format_date(date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    date = date.strftime('%a %d. %b')
    return "┤ " + date + " ├"

def display_current(current_hour):
    icon = format_hour(current_hour, current='current')
    for line in icon:
        sys.stdout.write(line + '\n')

def display_day(day):
    icon_morn = format_hour(day.morn)
    icon_aftn = format_hour(day.aftn)
    icon_even = format_hour(day.even)
    icon_nigh = format_hour(day.nigh)
    icon = []
    for i in range(5):
        icon.append("|" + icon_morn[i] + "|"  + icon_aftn[i] + "|"  + icon_even[i] + "|"  + icon_nigh[i] + "|")
    dateFmt = format_date(day.date)
    ret = [ "                                                       ┌─────────────┐                                                       ",
            "┌──────────────────────────────┬───────────────────────" + dateFmt + "───────────────────────┬──────────────────────────────┐",
            "│           Morning            │             Noon      └──────┬──────┘    Evening            │            Night             │",
            "├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤",
            "└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘"]
    ret = ret[:4] + icon + ret[4:]
    for line in ret:
        sys.stdout.write(line + '\n')

def main():
    parse_place(response)
    current_hour = Day.Time('0000', '0000')
    current_hour.parse_response(response=response, current_hour=True)
    display_current(current_hour)
    for i in range(num_of_days):
        date_of_day = datetime.date.today() + datetime.timedelta(days=i)
        d_string = date_of_day.strftime('%Y-%m-%d')
        day = Day(d_string)
        day.parse_response(response)
        display_day(day)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('q', nargs='?', default='Mumbai')
    parser.add_argument('num_of_days', nargs='?', type=int, default=3)
    args = parser.parse_args()
    q = str(args.q)
    num_of_days = int(args.num_of_days)
    url = 'http://api.worldweatheronline.com/free/v2/weather.ashx?q=%s&format=json&num_of_days=%d&key=%s' \
      % (q, num_of_days, key)
    r = requests.get(url)
    response = r.json()
    main()
