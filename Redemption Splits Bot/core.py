import discord
import asyncio
import json
import gspread
import help_text
import re
from doc_scan import DocScanner


class RedemptionBot(discord.Client):
    """Discord client for all Redemption Bot operations"""

    def __init__(self, doc, configs):
        super().__init__()
        self.token = configs['Bot Token']
        self.admin_name = configs['Admin Rank']
        self.doc = doc
        self.start_bot

    def start_bot(self):
        """Connects discord API"""
        loop = asyncio.get_event_loop()
        loop.create_task(self.start(self.token))
        try:
            loop.run_forever()
        finally:
            loop.stop()

    async def on_ready(self):
        print('Logged in successfully')
        print(self.user.name)
        print(self.user.id)
        print('-' * 5)


    async def on_message(self, message):
        """Bot commands via text inputs"""
        # Prevent bot responding to itself
        if message.author == self.user:
            return

        # Verify command was sent
        command = re.search(r'^![a-z]', message.content)
        if command is None:
            return

        # Prepares basic variables
        command = command.group()
        command = command.replace('!', '')
        msg = message.content.replace(f'!{command}', '').strip()
        author = message.author
        channel = message.channel
        guild = channel.guild
        isAdmin = str(author.roles).find(self.admin_name) != -1

        if command == 'check':
            # Request to find information on member
            print(f'User {author}: Checking for "{msg}"')
            await self.send_user(name=msg, author, channel, guild)
            
        if command == 'update' and isAdmin:
            print(f'User {author} updating: "{msg}"')

            # Updates user info (!update <name>, <split change>, <items>)
            inputs = msg.split(',')

            # Name:
            name = inputs[0].strip()
            # Delta Values:
            try: 
                delta = int(inputs[1])
            except(ValueError, SyntaxError, TypeError, IndexError):
                channel.send("Incorrect format, see !help")
                return
            # Gathers items
            items = ', '.join(inputs[2:]).strip() if len(inputs) > 2 else None

            # Updates sheet
            updates = self.doc.update_split(name, delta, items)
            if updates is None:
                channel.send(f'Cant find "{name}" on the sheet')
                return
            

            # Builds Embed
            prev_val, new_val, old_items, new_items = updates
            em_title = f"Splits increased by {delta}!"
            em_desc = f"-----"
            em_name = f"**Updating {name}'s stats'"
            em_url = None
            em_color = 0x01b0cf
            em_name_a = "Old Splits"
            em_val_a = "{:,}".format(prev_val)
            em_name_b = "New Splits"
            em_val_b = "{:,}".format(new_val)
            em_name_c = "Old Items"
            em_val_c = old_items
            em_name_d = "New Items"
            em_val_d = new_items

            player = await guild.get_member_named(name)
            if player is not None:
                em_url = str(player.avatar_url)

            embed = discord.Embed(
                title=em_title, 
                description=em_desc, 
                color=em_color
            )
            if em_url is not None:
                embed.set_author(name=em_author, icon_url=em_url)
            else:
                embed.set_author(name=em_author)
            embed.add_field(name=em_name_a, value=em_value_a, inline=True)
            embed.add_field(name=em_name_b, value=em_value_b, inline=True)
            embed.add_field(name=em_name_c, value=em_value_c, inline=False)
            embed.add_field(name=em_name_d, value=em_value_d, inline=False)

            await channel.send(embed=embed)
            
        if command == 'add' and isAdmin:
            pass
        if command == 'help':
            pass
        if command == 'exit':
            pass
        if command == 'test':
            await channel.send('This is a test')

    async def send_user(self, name, author, channel, guild):
        # Send embed with splits info

        values = self.doc.get_split(name)
        if values is None:
            await channel.send(f'Can\'t find someone named "{name}"')
            return

        # Prepares display values
        splits = values[1]
        days = values[3]
        rank = values[4]
        avatar = None

        player = await guild.get_member_named(name)
        if player is not None:
            avatar = str(player.avatar_url)
        
        # Build embed
        em_title = "**Current Split Value:**"
        em_desc = "{:,}".format(splits)
        em_color = 0x01b0cf
        em_author = f"{name}'s stats:"
        em_url = avatar
        em_name_a = "Current Rank: "
        em_value_a = f'{rank}'
        em_name_b = "Days in Clan: "
        em_value_b = f'{days} days'

        embed = discord.Embed(
            title=em_title, 
            description=em_desc, 
            color=em_color
        )
        if em_url is not None:
            embed.set_author(name=em_author, icon_url=em_url)
        else:
            embed.set_author(name=em_author)
        embed.add_field(name=em_name_a, value=em_value_a, inline=False)
        embed.add_field(name=em_name_b, value=em_value_b, inline=False)

        await channel.send(embed=embed)




        

    


if __name__ == "__main__":
    print("Initiating...")
    try:
        with open("configs.json", "r") as configs_file:
            print("configs.json file loaded")
            configs = json.loads(configs_file)
    except(FileNotFoundError):
        print('ERROR: Configs file not found, please consult Readme')
        return

    # Verifies configs
    reqs = ("Bot Token", "Admin Rank", "Spreadsheet URL", "Worksheet Name")
    if not all(req in configs for req in reqs):
        print('ERROR: Configs not formatting correctly, please consult the Readme')
        return

    # Opens document
    print('Loading Google sheet...')
    try:
        doc = DocScanner(configs["Spreadsheet URL"], configs["Worksheet Name"])
        print("Document loaded correctly")
    except(gspread.exceptions.NoValidUrlKeyFound): 
        print("ERROR: Document could not be loaded from the URL")
        invalid_input()
    except(gspread.exceptions.WorksheetNotFound):
        print("ERROR: Document could not find worksheet " + worksheet)
        invalid_input()
    except(FileNotFoundError):
        print("ERROR: Credentials file not found, please consult Readme")

    # Loads bot API
    print('Loading discord bot...')
    redemption_bot = RedemptionBot(doc, configs)
    
    # Shuts down
    print('Bot successfully shut down')
    print('Good bye')
    

