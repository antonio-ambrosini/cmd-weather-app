import os
import requests
import json
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


def get_location_key():
    load_dotenv("config/.env")
    return {
        'Authorization': f'Bearer {os.getenv("LOCATION_API_KEY")}'
    } 


def get_default_location():
    response = requests.get('http://ipinfo.io', get_location_key())
    return response.json()["city"]


def get_commands():
    return {
        "1" : "current weather",
        "2" : "3-day forecast",
        "3" : "7-day forecast",
        "4" : "sports",
        "5" : "astronomy"
    }


def display_commands(commands):
    for number,command in commands.items():
        print(f"{number}. {command.title()}")


def get_user_command():
    commands = get_commands()
    display_commands(commands)

    while True:
        command = input("Enter the number of the command that you want to perform: ").strip()

        if command in commands:
            return commands[command]
        
        print(f"Invalid command '{command}'. Please enter a valid command.") 


def get_url(command):
    base_url = "https://api.weatherapi.com/v1/"

    match command:
        case "current weather":
            return base_url + "current.json"


def create_request(command, settings):
    return {
        "url"    : get_url(command),
        "config" : {
            'key': get_key(),
            'q': settings["Location"]
        }
    }


def get_response(request):
    response = requests.get(request["url"], request["config"])
    return response.json()


def run_weather_app(settings):
    command = get_user_command()
    
    request = create_request(command, settings)

    response = get_response(request)

    print(response)


def main():
    user_settings = get_user_config()
    run_weather_app(user_settings)

    


if __name__ == "__main__":
    main()

    # also we can have an option to let the user change their settings if for
    # example they relocate

    # add section where once the request is made we check the response code using switch case and 
    # depending on the code we perform certain tasks