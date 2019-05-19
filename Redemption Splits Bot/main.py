import discord, json, string, gspread, sys, asyncio, time
from doc_scan import DocScanner
from datetime import datetime


def print_log(text):
    """Prints message with time in console and to log file"""
    curTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = curTime + " - " + str(text)
    print(message)
    with open("./Configs/Log.txt", "a") as logger:
        logger.write(message + "\n")


def invalid_input():
    print_log("Please correct in the configs file (Configs/config.json)\
    or delete the file to start the first time set-up again.")
    input()
    sys.exit()

# def first_time_setup():


print_log("=" * 10)
print_log("=" * 10)
print_log("Welcome! Initializing bot...")

# Loads configs file, if configs file does not exist initiates first time setup
try:
    print_log("Loading Configs File...")

    # Opens and loads configs file
    with open("./Configs/configs.json", "r") as configs_file:
        print_log("configs.json file loaded")
        configs = json.load(configs_file)

except(FileNotFoundError):
    # If Configs/configs.json does not exist, initiates FTS
    print_log("configs.json was not gound, initiating First Time Setup")


# Checks if Configs need to be updated
configs_update = False

# Verifies all entries exist. Does not confirm if entries valid
print_log("Verifying configuration settings...")
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
        print_log("Please enter a value for " + req + ": ")
        new_val = str(input()).strip()
        configs[req] = new_val
        configs_update = True
        print_log(req + ": " + configs[req])

# If value was updated
if configs_update is True:
    with open("./Configs/configs.json", "w") as file:
        json.dump(configs, file, indent=4)

print_log("If any of these values are incorrect, please modify or \
delete the congifs.json file located in the Configs folder, and \
restart the bot")

time.sleep(3)
print_log("-" * 5)

# Prepares to open sheet, if error encounters exists application
print_log("Preparing to open spreadsheet...")

# Grabs column values. If values are incorrect, exits prints an error 
characters = list(string.ascii_uppercase)
try:
    cName = characters.index(configs["Name Column"]) + 1
    cSplit = characters.index(configs["Split Column"]) + 1
    cItem = characters.index(configs["Items Column"]) + 1
    cDate = characters.index(configs["Date Column"]) + 1
except(ValueError):
    print_log("VALUE ERROR: Values for one or more of the colums is \
    incorrect!")
    invalid_input()

# Initiates spreadsheet or catches error when failed
url = configs["Spreadsheet URL"]
worksheet = configs["Worksheet Name"]
print_log("Loading document...")
try:
    doc = DocScanner(url, worksheet, [cName, cSplit, cItem, cDate])
    print_log("Document loaded correctly")
except(gspread.exceptions.NoValidUrlKeyFound): 
    print_log("ERROR: Document could not be loaded from the URL")
    invalid_input()
except(gspread.exceptions.WorksheetNotFound):
    print_log("ERROR: Document could not find worksheet " + worksheet)
    invalid_input()
except(FileNotFoundError):
    print_log("ERROR: Document could not be loaded from the URL")
    invalid_input()

# Initiates discord client
try:
    print_log("Initiating Discord API...")
    loop = asyncio.get_event_loop()
    client = discord.Client()
    TOKEN = configs["Bot Token"]
    # loop.run_until_complete(client.start(TOKEN))
except(discord.errors.LoginFailure):
    print_log("ERROR: Token was not accepted or correct")
    invalid_input()
except(discord.errors.GatewayNotFound, discord.errors.HTTPException):
    print_log("ERROR: Cannot load discord API")
    print_log("This can be due to lack of internet connection or API outage")
    print_log("Please try again later")


print_log("Exiting Script...")


'''
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
