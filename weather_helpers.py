import requests
from datetime import datetime

class Helpers:
    
    WEATHER_API_URL="http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s"
    FORECAST_API_URL="http://api.openweathermap.org/data/2.5/forecast?q=%s&appid=%s"
    forecast_for_5_days = {}

    def __init__(self, key):
        self.api_key = key 

    def get_temp(self, temp):
        return round(300 - temp)

    def get_weather_by_city(self, req_type, city):
        res = self.call_api(req_type, city)
        weather_forecast = res['weather'][0]['main']
        forecast_emoji = self.get_emoji(weather_forecast) 
        temp =  self.get_temp(res['main']['temp'])
        return (temp, forecast_emoji, res['weather'][0]['description'])

        
    def get_forecast_by_city(self, req_type, city):
        res = self.call_api(req_type, city)
        self.forecast_for_5_days = res['list']
        weather_forecasts = list()
        checked_day = 0
        for forecast in self.forecast_for_5_days:
            get_date = forecast['dt']
            date = datetime.fromtimestamp(get_date)
            day = datetime.date(date).day
            if checked_day != day:
                weather_forecast = forecast['weather'][0]['main']
                emoji = self.get_emoji(weather_forecast) 
                temp = self.get_temp(forecast['main']['temp'])
                weather_forecasts.append({
                    "city": city,
                    "data": get_date,
                    "weekday": date.strftime('%A'), 
                    "temp": str(temp), 
                    "emoji": emoji, 
                    "desc": forecast['weather'][0]['description']})
            checked_day = day    
        return weather_forecasts

    def next_day_forecast(self, chosen_date):
        morning = ''
        afternoon = ''
        evening = ''
        chosen_date = datetime.fromtimestamp(int(chosen_date)).date().day  
        for forecast in self.forecast_for_5_days:
            get_date = forecast['dt']
            date = datetime.fromtimestamp(get_date).date().day 
            if chosen_date == date:
                time = datetime.fromtimestamp(get_date).hour
                if time == 9:
                    emoji = self.get_emoji(forecast['weather'][0]['main']) 
                    temp = self.get_temp(forecast['main']['temp'])  
                    morning =  str(temp) + u'\N{DEGREE SIGN}' + "C " + emoji 
                if time == 15:
                    emoji = self.get_emoji(forecast['weather'][0]['main']) 
                    temp = self.get_temp(forecast['main']['temp'])  
                    afternoon =  str(temp) + u'\N{DEGREE SIGN}' + "C " + emoji 
                if time == 18:
                    emoji = self.get_emoji(forecast['weather'][0]['main']) 
                    temp = self.get_temp(forecast['main']['temp'])  
                    evening =  str(temp) + u'\N{DEGREE SIGN}' + "C " + emoji 
        return {"Morning": morning, "Afternoon":afternoon, "Evening":evening}

    def call_api(self, req_type, city):
        if req_type == "weather":
            url = self.WEATHER_API_URL
        else: 
            url = self.FORECAST_API_URL
        res = requests.get(url % (city, self.api_key))
        if res.status_code == 200:
            return res.json()

    def get_emoji(self, weather_forecast):
        forecast_emoji = ''
        if weather_forecast.lower().find('clear') > -1:
            forecast_emoji = '☀️'
        if weather_forecast.lower().find('cloud') > -1:
            forecast_emoji = '⛅️'
        if weather_forecast.lower().find('rain') > -1:
            forecast_emoji = '🌧'
        if weather_forecast.lower().find('snow') > -1:
            forecast_emoji = '🌨'
        return forecast_emoji  



