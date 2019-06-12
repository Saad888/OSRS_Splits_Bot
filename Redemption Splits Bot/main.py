import asyncio 
import discord
import json
import gspread
import help_text
from doc_scan import DocScanner
from datetime import datetime

client = discord.Client()



def validate_date(given_date):
    """Confirms format of the date to match dd/mm/YYYY or mm/dd/YYYY"""
    try:
        datetime.strptime(given_date, "%m/%d/%Y")
        return True
    except(ValueError, TypeError):
        return False


def first_time_setup():
    print("Please answer the following questions", 1)
    print("Please ensure Google API credentials are setup as per Readme", 1)
    print("Press enter to continue", 1)
    input()

    configs = {}
    print("1. Enter the Bot Token from the discord developement page (consult Readme for more info)")
    configs["Bot Token"] = str(input()).strip()

    print("2. Enter the EXACT name of the required rank for bot admin commands")
    configs["Admin Rank"] = str(input()).strip()

    print("3. Enter the exact URL of the spreadsheet")
    configs["Spreadsheet URL"] = str(input()).strip()

    print("4. Enter the exact name of the worksheet (or tab) of the google doc")
    configs["Worksheet Name"] = str(input()).strip()


    with open("configs.json", "w") as file:
        json.dump(configs, file, indent=4)

    return configs


# Initiates bot, verifies all settings then launches Docs API
try:
    print("=" * 10)
    print("=" * 10)
    print("Welcome! Initializing bot...")


    # Loads configs file, if configs file does not exist initiates first time setup
    try:
        print("Loading Configs File...")
        configs = {}
        # Opens and loads configs file
        with open("configs.json", "r") as configs_file:
            print("configs.json file loaded")
            configs = json.load(configs_file)
    # If Configs/configs.json does not exist, initiates FTS
    except(FileNotFoundError):
        print("configs.json was not found, initiating First Time Setup", 2)
        configs = first_time_setup()


    # Verifies all entries and google credentials file exist. 
    print("Verifying configuration settings...")
    try:
        file = open("credentials.json", "r")
        file.close()
    except(FileNotFoundError):
        print("credentials.json was not found, please consult the Readme")
        sys.exit()

    req_configs = (
        "Bot Token", 
        "Admin Rank",
        "Spreadsheet URL",
        "Worksheet Name",
    )
    try:
        for req in req_configs:
            configs[req]
    except(KeyError):
        print("One or more of the required configs missing.")
        invalid_input()

    print(json.dumps(configs, indent=4))
    print(help_text.Initial_Message, 3)

    print("-" * 5)

    # Prepares to open sheet, if error encounters exists application
    print("Preparing to open spreadsheet...")

    # Initiates spreadsheet or catches error when failed
    url = configs["Spreadsheet URL"]
    worksheet = configs["Worksheet Name"]
    print("Loading document...")
    try:
        doc = DocScanner(url, worksheet)
        print("Document loaded correctly")
    except(gspread.exceptions.NoValidUrlKeyFound): 
        print("ERROR: Document could not be loaded from the URL")
        invalid_input()
    except(gspread.exceptions.WorksheetNotFound):
        print("ERROR: Document could not find worksheet " + worksheet)
        invalid_input()
    except(FileNotFoundError):
        print("ERROR: Credentials file could not be found")
        print("Please obtain credentials as outlined in the Readme")

    admin_rank = configs["Admin Rank"]
    token = configs["Bot Token"]


except(SystemExit):
    print("Press enter to exit...")
    input()



@client.event
async def on_message(message):
    """Initiates command by bot based on inputs"""

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    author = message.author.name
    admin = str(message.author.roles).find(admin_rank) != -1

    incorrect_input_message = {
        "int": "Please enter a number without commas or symbols for the split.",
        "date": "Please make sure date format is M/D/YYYY."
    }

    try:
        if message.content.startswith("!splits "):
            print("User {}: {}".format(author, message.content))
            """Returns splits by user request"""
            msg = message.content
            username = msg.replace("!splits", "").strip()
            response = await doc.get_split(username)
            print(response)
            if response is None:
                reply = "Can't find the name {} in the list!".format(username)
            else:
                name = response[1]
                amount = response[0]
                reply = "{} has an item split of {:,}!".format(name, amount)
            await message.channel.send(reply)
            print(reply)
            
        if message.content.startswith("!update ") and admin is True:
            print("User {}: {}".format(author, message.content))
            """Adds split amount if user has admin rank"""
            msg = message.content

            # Splits input 
            request = msg.replace("!update", "").split(",")

            # Grabs name
            name = request[0].strip()

            # Gets splits value, if value was invalid prints appropriate message
            try:
                delta = int(request[1].strip())
            except(ValueError, SyntaxError, TypeError, IndexError):
                delta = None

            # Gets list of items if it exists
            item_list = ", ".join(request[2:]).strip() if len(request) > 2 else None
            
            # Updates split value and sends response to discord server
            if delta is not None:
                response = await doc.update_split(name, delta, item_list)
                if response is not None:
                    username = response[2]
                    prev_val = response[0]
                    new_val = response[1]
                    reply = "{}'s split changed from {:,} to {:,}.".format(
                        username,
                        prev_val, 
                        new_val
                    )
                else:
                    reply = "Can't find player {}".format(name)
            else:
                reply = incorrect_input_message["int"]

            await message.channel.send(reply)
            print(reply)

        if message.content.startswith("!add ") and admin is True:
            print("User {}: {}".format(author, message.content))
            """Adds user with inputs (!add_user name (split) (date) (items))"""
            msg = message.content

            # Splits input 
            request = msg.replace("!add", "").split(",")

            # Grabs name
            name = request[0].strip()
            reply = "The player {} was added".format(name)

            # Will prevent the doc API call if the provided inputs are incorrect
            validate_inputs = True
            splits = 0
            date = None
            item_list = ''

            # Gets and confirms split value
            if len(request) > 1:
                try:
                    split = int(request[1].strip())
                    reply += " with a split value of {}".format(split)
                except(TypeError, ValueError):
                    validate_inputs = False
                    reply = incorrect_input_message["int"]

            # Gets and confirms date value
            if (len(request) > 2) and (validate_inputs is True):
                date = request[2].strip()
                if validate_date(date) is True:
                    reply += ", and the join date {}".format(date)
                else:
                    validate_inputs = False
                    reply = incorrect_input_message["date"]

            # Gets list of items
            item_list = ", ".join(request[3:]).strip() if len(request) > 2 else ""

            if validate_inputs is True:
                reply += "!"
                added = await doc.add_user(name, splits, date, item_list)
                if added is False:
                    reply = "User {} already exists!".format(name)

            await message.channel.send(reply)
            print(reply)

    except(gspread.exceptions.APIError):
        reply = help_text.API_error
        await message.channel.send(reply)

    if message.content.startswith("!help"):
        print("User {}: {}".format(author, message.content))
        reply = help_text.help_reply
        if admin is True:
            reply = reply + "\n" + help_text.admin_help_reply
        await message.channel.send(reply)

    # Exit command - for debugging purposes only
    # if message.content.startswith("!exit"):
    #    await client.logout()


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")

# Initiates dicord API
try:
    print("Initiating Discord API...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.start(token))
except(discord.errors.LoginFailure):
    print("ERROR: Token was not accepted or correct")
    invalid_input()
except(discord.errors.GatewayNotFound, discord.errors.HTTPException):
    print("ERROR: Cannot load discord API")
    print("This can be due to lack of internet connection or API outage")
    print("Please try again later")
    sys.exit()
except(SystemExit):
    print("Press enter to exit...")
    input()
