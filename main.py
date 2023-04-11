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



many_metting_vichan_gif = "https://media.tenor.com/L9C-SHIR2AQAAAAd/%EB%B9%84%EC%B1%A4-viichan.gif"
many_many_metting_vichan_gif = "https://media.tenor.com/INrkO7KEe3QAAAAd/%EB%B9%84%EC%B1%A4-viichan.gif"
one_metting_vichan_gif = "https://media.tenor.com/INrkO7KEe3QAAAAd/%EB%B9%84%EC%B1%A4-viichan.gif"
no_metting_vichan_gif = "https://media.tenor.com/YLVttql_kgIAAAAC/%E3%82%94%E3%81%83%E3%81%A1%E3%82%83%E3%82%93-viichan.gif"


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')
    print(Token)

class Metting_member(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @discord.ui.button(label="멤버선택",  style=discord.ButtonStyle.grey)
    async def member_select(self, interaction:discord.Interaction, button:discord.ui.button):
        await interaction.response.send_message(content = "회의 등록이 완료됐어요.")

class Metting_time(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @discord.ui.button(label= "아침시간", style=discord.ButtonStyle.grey)
    async def metting_time_1(self, interaction:discord.Interaction, button:discord.ui.button):
        view = Metting_member()
        await interaction.response.send_message(content = "회의 등록이 완료되었어요!",view=view)

class Metting_place(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="2층 홈베이스", style=discord.ButtonStyle.grey)
    async def metting_place_1(self, interaction:discord.Interaction, button : discord.ui.button):
        view = Metting_time()
        await interaction.response.send_message(content= "회의할 시간을 선택해주세요", view=view)

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="회의 신청", style=discord.ButtonStyle.grey)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = Metting_place()
        member = interaction.user
        await interaction.response.send_message(content = "회의를 할 장소를 골라주세요.", view=view)


    @discord.ui.button(label="회의 목록", style = discord.ButtonStyle.blurple)
    async def menu2(self, interaction: discord.Interaction, button : discord.ui.Button):
        embed = discord.Embed(color=discord.Color.random())
        embed.set_author(name=f"This is a edited embed")
        print(interaction.author)

        if today_meet_count > 3:
            embed.set_image(url=(many_many_metting_vichan_gif))
            embed.add_field(name="Dill", value = "오늘은 회의로 가득한 날... 😭")
        
        elif today_meet_count > 1:
            embed.set_image(url=(many_metting_vichan_gif))
            embed.add_field(name="Dill", value = "오늘은 회의 많은 날.. 😓")

        elif today_meet_count == 1:
            embed.set_image(url=(one_metting_vichan_gif))
            embed.add_field(name="Diil", value = "오늘의 회의 1개 뿐인 날! 🎉")
        
        else :
            embed.set_image(url=(no_metting_vichan_gif))
            embed.add_field(name="Diil", value = "오늘은 회의 없는 날! 🎊")
        
        await interaction.response.send_message(embed=embed)
    
    @discord.ui.button(label="명령어", style = discord.ButtonStyle.red)
    async def menu3(self, interaction: discord.Interaction, button : discord.ui.Button):
        await interaction.response.send_message("Hello World")

@bot.command()
async def 띨챤(ctx):
    view = Menu()
    await ctx.reply("챤하 ~ 무엇을 도와드릴까요?", view=view)




bot.run(Token)