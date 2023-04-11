import discord
import os
import asyncio
import pytz

from discord.ext import commands
from dotenv import load_dotenv

from datetime import datetime

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
today_meet_count = 5

load_dotenv()
Token = os.getenv('Token')

embed=discord.Embed(timestamp=datetime.now(pytz.timezone('UTC')), color=0x54b800)

vivichan = "https://media.tenor.com/YLVttql_kgIAAAAC/%E3%82%94%E3%81%83%E3%81%A1%E3%82%83%E3%82%93-viichan.gif"
vivivichan = "https://media.tenor.com/INrkO7KEe3QAAAAd/%EB%B9%84%EC%B1%A4-viichan.gif"
many_metting_vichan = "https://media.tenor.com/L9C-SHIR2AQAAAAd/%EB%B9%84%EC%B1%A4-viichan.gif"
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')
    print(Token)

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="회의 신청", style=discord.ButtonStyle.grey)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content = "hello")

    @discord.ui.button(label="회의 목록", style = discord.ButtonStyle.blurple)
    async def menu2(self, interaction: discord.Interaction, button : discord.ui.Button):
        embed = discord.Embed(color=discord.Color.random())
        embed.set_author(name=f"This is a edited embed")
        
        await interaction.response.send_message(embed=embed)
    
    @discord.ui.button(label="명령어", style = discord.ButtonStyle.red)
    async def menu3(self, interaction: discord.Interaction, button : discord.ui.Button):
        await interaction.response.send_message("Hello World")

@bot.command()
async def 띨챤(ctx):
    view = Menu()
    await ctx.reply("챤하 ~ 무엇을 도와드릴까요?", view=view)

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