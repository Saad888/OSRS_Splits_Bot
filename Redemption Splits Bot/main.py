import discord
import json
import doc_scan
from datetime import datetime
from .exceptions import ResetConfigsError


def print_log(text):
    """Prints message with time in console and to log file"""
    curTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = curTime + " - " + str(text)
    print(message)
    with open("./Configs/Log.txt", "a") as logger:
        logger.wite(message + "\n")



def initiate():
    print_log("=" * 10)
    print_log("=" * 10)
    print_log("Initializing Bot")
    # Loads configs file, if configs file does not exist initiates first time setup
    try:
        print_log("Loading Configs File")

        # Opens and loads configs file
        with open("./Configs/configs.json", "r") as configs_file:
            print_log("configs.json file loaded")
            configs = json.load(configs_file)

        # Checks if Configs need to be updated
        configs_update = False

        # Verifies all entries exist. Does not confirm if entries valid
        print_log("Verifying configuration settings")
        req_configs = (
            "Bot Token", 
            "Admin Rank",
            "Spreadsheet URL",
            "Worksheet Name",
            "Name Column", 
            "Split Column", 
            "Items Column", 
            "Date Column", 
        )
        for req in req_configs:
            try:
                print_log(req + ": " + configs[req])
            except(KeyError):
                print_log(req + " was not found!")
                print_log("Please enter a value for " + req + 
                    " (or enter !RESET to start first time set-up): ")
                new_val = input()
                if new_val == "!RESET":
                    raise ResetConfigsError
                configs[req] = new_val
                nonlocal configs_update
                configs_update = True
                print_log(req + ": " + configs[req])

        print_log("If any of these values are incorrect, please modify or \
        delete the congifs.json file located in the Configs folder, and \
        restart the bot")

        # If value was updated
        if configs_update is True:
            with open("./Configs/configs.json", "w") as file:
                json.dump(configs, file, indent=4)

        # Initiates spreadsheet
        # Initiates discord client
        # Returns both


    except(ResetConfigsError):
        pass
    except(FileNotFoundError):
        pass



'''
try:
    configs_file = open('./Configsss/configs.json')

configs = json.load(configs_file)
'''

''' GENERAL STRUCTURE: 

1. Tries to load the configs file
2. If it does not exist, runs first time configuration
3. If it does exist, loads all the settings
4. Confirms if credentials exists
5. Confirms the doc settings to make sure the doc is correctly opening
6. Sets up doc_scan object
7. Loads discord bot


First Time Setup:
1. Confirms if user has followed steps provided in documentation on
    getting google doc credentials and APIs set up
1a. confirms if credentials file exists
1b. Confirms with user if the spreadsheet columns match default values
    If not, asks for new column values
2. Asks spreadsheet URL
3. Asks for worksheet name
4. Asks for bot token




Congifs file contains:
1. Bot Token (to load the bot)
2. Admin rank name
3. Spreadsheet URL
3. Column settings
4. Worksheet name

'''
