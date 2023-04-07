import discord
import os
import asyncio
import pytz

from discord.ext import commands
from dotenv import load_dotenv

from datetime import datetime

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


load_dotenv()
Token = os.getenv('Token')

embed=discord.Embed(timestamp=datetime.now(pytz.timezone('UTC')), color=0x54b800)

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

@bot.command()
async def 회의공지(ctx):
    await ctx.channel.send("회의를 할 장소를 15초내로 적어주세요.")

    try:
        message = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=15.0)
    except asyncio.TimeoutError:
        await ctx.channel.send("15초가 지났어요. 명령어를 다시 실행시켜주세요.")
    
    else :
        if message.content is True :
            await ctx.channel.send(message.content)
        else :
            await ctx.channel.send("장소를 다시 입력해주세요.")

@bot.command()
async def 회의확인(ctx):
    await ctx.channel.send(file=discord.File("resource\회의확인.png"), embed=embed)



bot.run(Token)