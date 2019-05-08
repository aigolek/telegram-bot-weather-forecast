import telebot
from telebot import types
import weather_helpers as helper
from datetime import datetime

API_KEY = 'xxx'
bot = telebot.TeleBot("xxx") 
weather = helper.Helpers(API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    bot.reply_to(message, "Hello " + user_name + "! Type any city to find out the weather!" + u'\U0001F31E' + u'\U0001F324' + u'\U0001F327')

@bot.message_handler(content_types=['text'])
def send_city(message):
    chat_id=message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    if message:
        city = message.text
        forecast = weather.get_weather_by_city("weather", city)
        forecast_5_days = weather.get_forecast_by_city("forecast", city)
        bot.send_message(chat_id, "Current temperature in " + city + " is " + str(forecast[0]) + u'\N{DEGREE SIGN}' + "C " + forecast[1] + forecast[2])  
        for forecast in forecast_5_days:
            daily_forecast = forecast['weekday'] + " " + forecast['temp'] + u'\N{DEGREE SIGN}' + "C " + forecast['emoji']
            btn=types.InlineKeyboardButton(daily_forecast, callback_data=forecast['data'])
            keyboard.add(btn) 
        bot.send_message(chat_id, "Forecast  for the next 5 days: ", reply_markup=keyboard)  

@bot.callback_query_handler(func=lambda call: True)
def handleInlineButton(call):
    chat_id=call.message.chat.id
    if call.message:
        forecast = weather.next_day_forecast(call.data)
        bot.send_message(chat_id, "Detail view for " 
        + str(datetime.fromtimestamp(int(call.data)).date())
        + "\n Morning "
        + forecast['Morning'] 
        + "\n Afternoon " 
        + forecast['Afternoon']
        + "\n Evening " 
        + forecast['Evening']) 

bot.polling()    

