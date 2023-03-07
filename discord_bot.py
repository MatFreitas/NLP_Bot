import os
import re
import discord
import requests
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=os.getenv('GUILD_NAME'))
    channel = discord.utils.get(guild.text_channels, name=os.getenv('CHANNEL_NAME'))
    # await channel.send('O bot está online!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == '!author':
        await message.channel.send('I was created by Matheus Freitas. whose email is matheusfs2@al.insper.edu.br')

    if message.content.lower() == '!source':
        await message.channel.send('Here is the repository with my source code: https://github.com/MatFreitas/NLP_Bot')

    if message.content.lower() == '!help':
        await message.channel.send("!run <country> native_name: returns country's native name.\n"\
                                   "!run <country> currency: returns country's currency.\n"\
                                   "!run <country> capital: returns country's capital.\n"\
                                   "!run <country> flag: returns country's flag description.\n"\
                                   "If country name is a compound name, you can write it partially."\
                                   "Info obtained at: https://restcountries.com/")

    if message.content.lower()[:4] == '!run':
        args = message.content.lower().split()[1:]

        # Making first letter of country to be a capital letter
        args[0] = args[0][0].upper() + args[0][1:]
    
        # Validating with regex if arguments are valid
        for arg in args:
            if re.fullmatch("\w[^\d]+", arg) is None:
                await message.channel.send(f"'{arg}' does not seem to be a valid argument.")

        
        response = requests.get(f"https://restcountries.com/v3.1/name/{args[0]}").json()[0]

        if args[1] == "native_name":
            info = list(response["name"]["nativeName"].values())[0]["common"]
            await message.channel.send(f"{args[0]}'s native name is {info}.")

        elif args[1] == "currency":
            currency = list(response["currencies"].values())[0]["name"]
            symbol = list(response["currencies"].values())[0]["symbol"]
            await message.channel.send(f"{args[0]}'s currency is {currency}, which is represented with '{symbol}'.")
        
        elif args[1] == "capital":
            info = list(response["capital"])[0]
            await message.channel.send(f"{args[0]}'s capital is {info}.")  

        elif args[1] == "flag":
            try:
                info = response["flags"]["alt"]
                await message.channel.send(info)     
            except:
                await message.channel.send(f"There does not seem to have a description to {args[0]}'s flag yet!")     

        else:
            await message.channel.send(f"'{args[1]}' is not a valid option! Try using '!help' to understand how to use '!run'.")     

client.run(os.getenv('TOKEN'))