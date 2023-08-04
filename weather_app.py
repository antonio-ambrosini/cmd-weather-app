import os
import requests
import json
from dotenv import load_dotenv



def get_key():
    load_dotenv("config/.env")
    return os.getenv("API_KEY")


def get_user_config():

    if os.path.exists("config/user_settings.json"):
        return read_user_config()
    
    else:
        print("It looks like this is your first time using our services.")
        return config_or_default()


def read_user_config():
    with open("config/user_settings.json", "r") as settings:
        config = json.load(settings)
    
    print(f"Welcome back {config['Name']}!")
    return config


def create_user_config():
    
    with open("config/user_settings.json", 'w') as settings:
        json.dump(prompt_user_for_config(), settings, indent=4)
    
    # when adding the GUI there should be a settings button which will allow the user to change
    # their settings
    print("""Your settings has been saved. If you made a mistake or would like to change your settings
you can go to the settings menu and make the necessary changes.""")


def get_default_config():
    return {
        "Name"     : "New User",
        "Location" : ""   
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
        "Location" : "What is your current location?"
    }

    print("Let's configure your settings...\n")
    for key,value in data.items():
        data[key] = input(value + "\n")        

    return data


def main():
    user_settings = get_user_config()



if __name__ == "__main__":
    main()
    # configure user settings - ask user what their location is etc, and then
    # store this info. then each time the user runs the program we can read their settings
    # or let them configure it if it's their first time

    # also we can have an option to let the user change their settings if for
    # example they relocate