import discord
import os
import asyncio
import pytz
import time 

from discord.ext import commands, tasks
from discord.ui import Select, View
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from datetime import datetime,date


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
today_meet_count = 0
db_count = 0
meeting_subject = ""
meeting_time = ""
meeting_place = ""
meeting_member = []



load_dotenv()
Token = os.getenv('Token')
database_url = os.getenv('database_url')
guild_url = os.getenv('guild_url')
channel_url = os.getenv('channel_url')

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
    
    ref = str(date.today())
    ref_cut = ref[5:10]
    print(ref_cut)


@bot.command()
async def 챤하(ctx):
    view = Menu()
    await ctx.reply("챤하 ~ 무엇을 도와드릴까요?", view=view)

class SelectPage2(discord.ui.View):
    @discord.ui.select(
            placeholder = "회의 멤버를 선택해주세요.",
            min_values = 1,
            max_values = 16,
            options=[
                discord.SelectOption(label="김시훈", description="백엔드", emoji="🐱"),
                discord.SelectOption(label="전승원", description="백엔드", emoji="🐱"),
                discord.SelectOption(label="윤지빈", description="백엔드", emoji="🐱"),
                discord.SelectOption(label="조재영", description="백엔드", emoji="🐱"),
                discord.SelectOption(label="노현주", description="백엔드", emoji="🐱"),
                discord.SelectOption(label="박주홍", description="백엔드", emoji="🐱"),
                discord.SelectOption(label="김희망", description="백엔드", emoji="🐱"),
                discord.SelectOption(label="김태오", description="백엔드", emoji="🐱"),
                discord.SelectOption(label="변찬우", description="프론트엔드", emoji="🦄"),
                discord.SelectOption(label="강경민", description="프론트엔드", emoji="🦄"),
                discord.SelectOption(label="박영재", description="프론트엔드", emoji="🦄"),
                discord.SelectOption(label="송현우", description="프론트엔드", emoji="🦄"),
                discord.SelectOption(label="서주미", description="프론트엔드", emoji="🦄"),
                discord.SelectOption(label="이태랑", description="프론트엔드", emoji="🦄"),
                discord.SelectOption(label="이운린", description="프론트엔드", emoji="🦄"),
                discord.SelectOption(label="노가성", description="DevOps", emoji="🌥")
        ]
        )

    async def select_callback(self, select, interaction):
        global db_count
        global meeting_member

        print(interaction.values)
        meeting_member += interaction.values
        meeting_member.remove("다음페이지")
        print(meeting_member)
        
        db_count += 1
        ref =  db.reference(meeting_date + "/" + str(db_count))
        ref.update({'주제': str(meeting_subject)})
        ref.update({'날짜': str(meeting_date)})
        ref.update({'시간': meeting_time})
        ref.update({'장소': meeting_place})
        ref.update({'멤버': meeting_member})
        await select.response.send_message("회의 등록이 완료됐어요.")

    
class SelectPage1(discord.ui.View):
    @discord.ui.select(
            placeholder = "회의 멤버를 선택해주세요.",
            min_values = 1,
            max_values = 19,
            options=[
                discord.SelectOption(label="이현빈", description="안드로이드", emoji="🤖"),
                discord.SelectOption(label="김현승", description="안드로이드", emoji="🤖"),
                discord.SelectOption(label="백승민", description="안드로이드", emoji="🤖"),
                discord.SelectOption(label="박성현", description="안드로이드", emoji="🤖"),
                discord.SelectOption(label="김대진", description="안드로이드", emoji="🤖"),
                discord.SelectOption(label="정찬우", description="안드로이드", emoji="🤖"),
                discord.SelectOption(label="채종인", description="안드로이드", emoji="🤖"),
                discord.SelectOption(label="최형우", description="IOS", emoji="🍎"),
                discord.SelectOption(label="김성훈", description="IOS", emoji="🍎"),
                discord.SelectOption(label="박준서", description="IOS", emoji="🍎"),
                discord.SelectOption(label="선민재", description="IOS", emoji="🍎"),
                discord.SelectOption(label="안강호", description="IOS", emoji="🍎"),
                discord.SelectOption(label="정윤서", description="IOS", emoji="🍎"),
                discord.SelectOption(label="임준화", description="IOS", emoji="🍎"),
                discord.SelectOption(label="안진형", description="디자인", emoji="🎨"),
                discord.SelectOption(label="김준", description="디자인", emoji="🎨"),
                discord.SelectOption(label="강민수", description="디자인", emoji="🎨"),
                discord.SelectOption(label="김하온", description="디자인", emoji="🎨"),
                discord.SelectOption(label="다음페이지", description="다음 페이지로 이동합니다.", emoji="⏭")
            ]
        )
    async def select_callback(self, select, interaction):
        global db_count
        global meeting_member

        meeting_member = interaction.values

        print(meeting_member)

        if "다음페이지" in interaction.values:
            view = SelectPage2()
            await select.response.send_message(content = "회의에 참석할 멤버를 선택해주세요.", view=view)
        else :
            db_count += 1
            ref =  db.reference(meeting_date + "/" + str(db_count))
            ref.update({'주제': str(meeting_subject)})
            ref.update({'날짜': str(meeting_date)})
            ref.update({'시간': meeting_time})
            ref.update({'장소': meeting_place})
            ref.update({'멤버': meeting_member})
            await select.response.send_message("회의 등록이 완료되었어요.")

        

class Metting_time(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label= "아침시간", style=discord.ButtonStyle.grey)
    async def metting_time_1(self, interaction:discord.Interaction, button:discord.ui.button):
        global meeting_time

        view = SelectPage1()
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
        global meeting_date

        view = Metting_place()
        member = interaction.user
        await interaction.response.send_message(content = "회의 주제를 알려주세요.")
        
        try:
            message = await bot.wait_for("message", check=lambda message: interaction.user == member, timeout=15.0)
        except asyncio.TimeoutError:
            await message.channel.send("15초가 지났어요. 명령어를 다시 실행시켜주세요.")

        else :
            meeting_subject = message.content
            await message.channel.send(content= "회의할 날짜를 말해주세요. 이때 04-14 같은 형식으로 입력해주셔야해요!")
            
            try:
                message = await bot.wait_for("message", check=lambda message: interaction.user == member, timeout=15.0)
            except asyncio.TimeoutError:
                await message.channel.send("15초가 지났어요. 명령어를 다시 실행시켜주세요.")
            else:
                meeting_date = message.content
                if len(meeting_date) != 15 or meeting_date[3:3] != "-":
                    await message.channel.send("잘못된 정보를 입력하셨어요. 명령어를 다시 실행시켜주세요.")
                else:   
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




bot.run(Token)