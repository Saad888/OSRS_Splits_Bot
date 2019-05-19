# Copied text to test bot
import discord
import json
import asyncio

with open('configs.json') as file:
    configs = json.load(file)


TOKEN = configs["Bot Token"]
#TOKEN = '54fdsafdsaf1dsa'
client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.channel.name}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!exit'):
        await client.logout()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.start(TOKEN))
except(discord.errors.LoginFailure):
    print("saved")

'''
try:

    
    #asyncio.run(bot_run(TOKEN))
except(discord.errors.LoginFailure):
    print("DAUYMM GENIA")
'''