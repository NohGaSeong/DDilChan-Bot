import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
load_dotenv()
Token = os.getenv('Token')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')
    print(Token)

@bot.command()
async def ping(ctx):
    await ctx.send("pong")



bot.run(Token)