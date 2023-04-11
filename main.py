import discord
import os
import asyncio
import pytz

from discord.ext import commands
from discord.ui import Select, View
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from datetime import datetime


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
today_meet_count = 0
meeting_subject = ""
meeting_time = ""
meeting_place = ""
select_member = []

load_dotenv()
Token = os.getenv('Token')
database_url = os.getenv('database_url')

embed=discord.Embed(timestamp=datetime.now(pytz.timezone('UTC')), color=0x54b800)

cred = credentials.Certificate("ddillchan-firebase-adminsdk-r1wuk-712b7d43b7.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : database_url
})


many_metting_vichan_gif = "https://cdn.discordapp.com/attachments/953156775262167111/1095244923550302208/WASTED.png"
many_many_metting_vichan_gif = "https://cdn.discordapp.com/attachments/953156775262167111/1095244923034415114/CRYING_CHAN2.gif"
one_metting_vichan_gif = "https://cdn.discordapp.com/attachments/953156775262167111/1095244921922924544/RUNNING_CHAN.gif"
no_metting_vichan_gif = "https://cdn.discordapp.com/attachments/953156775262167111/1095244918584266792/VIICHAN_ZERO2.gif"


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')
    print(Token)
    
    dir = db.reference()

class Metting_member(discord.ui.Select):
    def __init__(self):
        options=[discord.SelectOption(label="이현빈", description="안드로이드", emoji="🤖"),
                discord.SelectOption(label="변찬우", description="안드로이드", emoji="🤖"),
                discord.SelectOption(label="노가성", description="안드로이드", emoji="🤖"),
                discord.SelectOption(label="정은성", description="안드로이드", emoji="🤖"),
                discord.SelectOption(label="김동현", description="안드로이드", emoji="🤖")]
        super().__init__(placeholder="회의 인원을 선택해주세요!", options=options, min_values=2, max_values=5, row=2)
    
    async def callback(self, interaction: discord.Interaction):
        select_member = (','.join(self.values))
        await interaction.response.send_message(content = f"{self.values}")

class Select(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Metting_member())

class Metting_time(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label= "아침시간", style=discord.ButtonStyle.grey)
    async def metting_time_1(self, interaction:discord.Interaction, button:discord.ui.button):
        global metting_time

        view = Select()
        meeting_time = "아침시간"
        await interaction.response.send_message(content = "회의에 참석할 멤버를 선택해주세요.", view=view)

class Metting_place(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="2층 홈베이스", style=discord.ButtonStyle.grey)
    async def metting_place_1(self, interaction:discord.Interaction, button : discord.ui.button):
        global meeting_place

        view = Metting_time()
        meeting_place = "2층 홈베이스"
        await interaction.response.send_message(content= "회의할 시간을 선택해주세요", view=view)


class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="회의 신청", style=discord.ButtonStyle.grey)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        global meeting_subject
        global message

        view = Metting_place()
        member = interaction.user
        await interaction.response.send_message(content = "회의 주제를 알려주세요.")
        
        try:
            message = await bot.wait_for("message", check=lambda message: interaction.user == member, timeout=15.0)
        except asyncio.TimeoutError:
            await message.channel.send("15초가 지났어요. 명령어를 다시 실행시켜주세요.")

        else :
            meeting_subject = message.content
            await message.channel.send(content= "회의할 날짜를 말해주세요")
            
            try:
                message = await bot.wait_for("message", check=lambda message: interaction.user == member, timeout=15.0)
            except asyncio.TimeoutError:
                await message.channel.send("15초가 지났어요. 명령어를 다시 실행시켜주세요.")
            else:
                meeting_date = message.content
                view = Metting_place()
                await message.channel.send(content = "회의할 장소를 선택해주세요.", view=view)



    @discord.ui.button(label="회의 목록", style = discord.ButtonStyle.blurple)
    async def menu2(self, interaction: discord.Interaction, button : discord.ui.Button):
        embed.set_author(name="띨챤의 회의 관리 리스트")

        if today_meet_count > 3:
            embed.set_image(url=(many_many_metting_vichan_gif))
            on_embed_text = "오늘은 회의로 가득한 날... 😭"
        
        elif today_meet_count > 1:
            embed.set_image(url=(many_metting_vichan_gif))
            on_embed_text = "오늘은 회의 많은 날.. 😓"

        elif today_meet_count == 1:
            embed.set_image(url=(one_metting_vichan_gif))
            on_embed_text = "오늘의 회의 1개 뿐인 날! 🎉"
        
        else :
            embed.set_image(url=(no_metting_vichan_gif))
            on_embed_text = "오늘은 회의 없는 날! 🎊"
        
        await interaction.response.send_message(content=on_embed_text, embed=embed)
    
    @discord.ui.button(label="명령어", style = discord.ButtonStyle.red)
    async def menu3(self, interaction: discord.Interaction, button : discord.ui.Button):
        await interaction.response.send_message("Hello World")

@bot.command()
async def 띨챤(ctx):
    view = Menu()
    await ctx.reply("챤하 ~ 무엇을 도와드릴까요?", view=view)




bot.run(Token)