import os
import requests
import json
import datetime
from dotenv import load_dotenv


def get_key():
    load_dotenv("config/.env")
    return os.getenv("WEATHER_API_KEY")


def get_user_config():

    if os.path.exists("config/user_settings.json"):
        return read_user_config()
    
    else:
        print("It looks like this is your first time using our services.")
        return config_or_default()


def read_user_config():
    with open("config/user_settings.json", "r") as settings:
        config = json.load(settings)
    
    print(f"Welcome back {config['Name'].title()}!")
    return config


def create_user_config():
    config = prompt_user_for_config()

    with open("config/user_settings.json", 'w') as settings:
        json.dump(config, settings, indent=4)
    
    # when adding the GUI there should be a settings button which will allow the user to change
    # their settings
    print("""Your settings has been saved. If you made a mistake or would like to change your settings
you can go to the settings menu and make the necessary changes.""")

    return config


def get_default_config():
    return {
        "Name"     : "New User",
        "Location" : get_default_location()   
        }


def config_or_default():

    # when adding GUI to the project the user should get a box window where they only have two
    # buttons which will be configure or default
    decision = input("""Would you like to configure your own settings or use our default
settings based on your current location? (configure/default):\n""")

    match decision.lower():

        case "configure":
            return create_user_config()
        
        case "default":
            return get_default_config()
        
        case _:
            print(f"Error! '{decision}' is not a valid answer.")
            config_or_default()


def prompt_user_for_config():
    data = {
        "Name"     : "Please enter your name:",
        "Location" : "What city are you located in?"
    }

    print("Let's configure your settings...\n")
    for key,value in data.items():
        data[key] = input(value + "\n").lower().strip()       

    return data


def get_default_location():
    response = requests.get('http://ipinfo.io')
    return response.json()["city"]


def create_request(settings):
    return {
        "url"     : "https://api.weatherapi.com/v1/forecast.json",
        "config"  : {
            'key' : get_key(),
            'q'   : settings['Location'],
            'days': 3
        }
    }


def get_response(request):
    response = requests.get(request["url"], request["config"])
    return response.json()
    

def get_current_weather(weather_data):
    return {
        'city': weather_data['location']['name'],
        'province': weather_data['location']['region'],
        'country': weather_data['location']['country'],

        'temperature': weather_data['current']['temp_c'],
        'weather-description': weather_data['current']['condition']['text'],
        'icon': weather_data['current']['condition']['icon'],
        'wind-speed': weather_data['current']['wind_kph'],
        'wind-direction': weather_data['current']['wind_dir'],
        'humidity': weather_data['current']['humidity'],
        'feels-like': weather_data['current']['feelslike_c'],
        'uv': weather_data['current']['uv'],

        'last-updated': weather_data['current']['last_updated']
    }


def get_hourly_forecast_for_today(weather_data):
    current_hour = str(datetime.datetime.now())[:14] + "00"
    today = weather_data['forecast']['forecastday'][0]['hour']
    
    for index, hour in enumerate(today):
        if current_hour == hour['time']:
            return today[index + 1:]


def get_forecast_from_tomorrow(weather_data):

    # overall weather data for the day is stored in weather_data['forecast']['forecastday'][num]['day']

    return {
        'tomorrow'           : weather_data['forecast']['forecastday'][1],
        'day after tomorrow' : weather_data['forecast']['forecastday'][2]
    }



def main():
    user_settings = get_user_config()
    request = create_request(user_settings)
    response = get_response(request)

    current_weather = get_current_weather(response)
    todays_hourly_forecast = get_hourly_forecast_for_today(response)
    forecast_from_tomorrow = get_forecast_from_tomorrow(response)

    print(current_weather)
    
    #display data on tkinter gui

if __name__ == "__main__":
    main()

    # also we can have an option to let the user change their settings if for
    # example they relocate

    # let the default display have today's weather forecast and then if the user wants to get any
    # other forecast data they can request for it or click somewhere and get it