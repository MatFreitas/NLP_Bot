import os
import discord
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
    await channel.send('O bot está online!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == '!author':
        await message.channel.send('Eu fui criado pelo Matheus Freitas, cujo email é mat.f.santana@uol.com.br!')

client.run(os.getenv('TOKEN'))