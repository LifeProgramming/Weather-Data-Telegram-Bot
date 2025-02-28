import telebot
import app
from apiKey import apiKey
import datetime
import pytz

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
BOT_TOKEN = apiKey

bot = telebot.TeleBot(BOT_TOKEN)

def format_weather_data(weather_data):
    """Formats the weather data from your module into a user-friendly string."""

    if weather_data is None:
        return "Sorry, I couldn't retrieve the weather data."

    try:
        temp_celsius = weather_data["temp_celsius"]
        temp_kelvin = weather_data["temp_kelvin"]
        feels_like_celsius = weather_data["feels_like_celsius"]
        feels_like_kelvin = weather_data["feels_like_kelvin"]
        humidity = weather_data["humidity"]
        description = weather_data["description"].capitalize()
        sunrise_time = weather_data["sunrise_time"]
        sunset_time = weather_data["sunset_time"]

        weather_string = (
            f"Weather: {description}\n"
            f"Temperature: {temp_celsius:.2f}°C ({temp_kelvin}K)\n"
            f"Feels like: {feels_like_celsius:.2f}°C ({feels_like_kelvin}K)\n"
            f"Humidity: {humidity}%\n"
            f"Sunrise: {sunrise_time}\n"
            f"Sunset: {sunset_time}"
        )
        return weather_string

    except KeyError as e:
        print(f"Missing key in weather data: {e}")
        return "Sorry, there was an issue processing the weather data. Please try again later."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred. Please try again later."

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Sends a welcome message and instructions."""
    bot.reply_to(message, "Hi! I'm a weather bot. Just send me the name of a city or country, and I'll tell you the weather.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handles user messages and retrieves weather data."""
    city = message.text
    try:
        weather_data = app.weatherData(city) #Calls your weather module
        if weather_data:
            weather_string = format_weather_data(weather_data)
            bot.reply_to(message, weather_string)
        else:
            bot.reply_to(message, "Sorry, I couldn't find the weather for that city. Please check the city name and try again.")
    except Exception as e:
        print(f"Error processing city: {e}")
        bot.reply_to(message, "Sorry, I couldn't find the weather for that city. Please check the city name and try again.")

if __name__ == '__main__':
    print("Bot started...")
    bot.infinity_polling()