import discord
import os
import asyncio
import pytz
import time 
import requests

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
many_many_metting_vichan_gif = "https://cdn.discordapp.com/attachments/953156775262167111/1095244923550302208/WASTED.png"
many_metting_vichan_gif = os.getenv('many_metting_vichan_gif')
one_metting_vichan_gif = os.getenv('one_metting_vichan_gif')
no_metting_vichan_gif = os.getenv('no_metting_vichan_gif')


embed=discord.Embed(timestamp=datetime.now(pytz.timezone('UTC')), color=0x54b800)

cred = credentials.Certificate("ddillchan-firebase-adminsdk-r1wuk-712b7d43b7.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : database_url
})

ref_today = str(date.today())
    
ref_today_cut = ref_today[5:10]

ref = db.reference(f"{ref_today_cut}")
ref_get = ref.get()

member_dict = db.reference('멤버 아이디')
member_dict_get = member_dict.get()

@bot.event
async def on_ready():
    global today_meet_count
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')
    print(Token)
    print(member_dict_get)

    for i in range(len(ref_get)-1):
        embed.add_field(name=f"{ref_get[i+1].get('주제')}", 
                        value = f"날짜 : {ref_get[i+1].get('날짜')}\n"
                            + f"회의시간: {ref_get[i+1].get('시간')}\n"
                            + f"회의장소: {ref_get[i+1].get('장소')}\n"
                            + f"참석인원: {ref_get[i+1].get('멤버')}\n",
                        inline=False)
        today_meet_count += 1

    every_hour_notice.start()
    
    
        

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

    @discord.ui.button(label= "점심시간", style=discord.ButtonStyle.grey)
    async def metting_time_2(self, interaction:discord.Interaction, button:discord.ui.button):
        global meeting_time

        view = SelectPage1()
        meeting_time = "점심시간"

        await interaction.response.send_message(content = "회의에 참석할 멤버를 선택해주세요.", view=view)
    
    @discord.ui.button(label= "저녁시간", style=discord.ButtonStyle.grey)
    async def metting_time_3(self, interaction:discord.Interaction, button:discord.ui.button):
        global meeting_time

        view = SelectPage1()
        meeting_time = "저녁시간"

        await interaction.response.send_message(content = "회의에 참석할 멤버를 선택해주세요.", view=view)

    @discord.ui.button(label= "7교시", style=discord.ButtonStyle.grey)
    async def metting_time_4(self, interaction:discord.Interaction, button:discord.ui.button):
        global meeting_time

        view = SelectPage1()
        meeting_time = "7교시"

        await interaction.response.send_message(content = "회의에 참석할 멤버를 선택해주세요.", view=view)

    @discord.ui.button(label= "8교시", style=discord.ButtonStyle.grey)
    async def metting_time_5(self, interaction:discord.Interaction, button:discord.ui.button):
        global meeting_time

        view = SelectPage1()
        meeting_time = "8교시"

        await interaction.response.send_message(content = "회의에 참석할 멤버를 선택해주세요.", view=view)
    
    @discord.ui.button(label= "9교시", style=discord.ButtonStyle.grey)
    async def metting_time_6(self, interaction:discord.Interaction, button:discord.ui.button):
        global meeting_time

        view = SelectPage1()
        meeting_time = "9교시"

        await interaction.response.send_message(content = "회의에 참석할 멤버를 선택해주세요.", view=view)

    @discord.ui.button(label= "10교시", style=discord.ButtonStyle.grey)
    async def metting_time_7(self, interaction:discord.Interaction, button:discord.ui.button):
        global meeting_time

        view = SelectPage1()
        meeting_time = "10교시"

        await interaction.response.send_message(content = "회의에 참석할 멤버를 선택해주세요.", view=view)

    
    @discord.ui.button(label= "11교시", style=discord.ButtonStyle.grey)
    async def metting_time_8(self, interaction:discord.Interaction, button:discord.ui.button):
        global meeting_time

        view = SelectPage1()
        meeting_time = "11교시"

        await interaction.response.send_message(content = "회의에 참석할 멤버를 선택해주세요.", view=view)
        
    @discord.ui.button(label= "기숙사 자습시간", style=discord.ButtonStyle.grey)
    async def metting_time_9(self, interaction:discord.Interaction, button:discord.ui.button):
        global meeting_time

        view = SelectPage1()
        meeting_time = "기숙사 자습시간"

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
    
    @discord.ui.button(label="3층 홈베이스", style=discord.ButtonStyle.grey)
    async def metting_place_2(self, interaction:discord.Interaction, button : discord.ui.button):
        global meeting_place

        view = Metting_time()
        meeting_place = "3층 홈베이스"
        await interaction.response.send_message(content= "회의할 시간을 선택해주세요", view=view)

    @discord.ui.button(label="4층 홈베이스", style=discord.ButtonStyle.grey)
    async def metting_place_3(self, interaction:discord.Interaction, button : discord.ui.button):
        global meeting_place

        view = Metting_time()
        meeting_place = "4층 홈베이스"
        await interaction.response.send_message(content= "회의할 시간을 선택해주세요", view=view)

    @discord.ui.button(label="빅데이터실", style=discord.ButtonStyle.grey)
    async def metting_place_4(self, interaction:discord.Interaction, button : discord.ui.button):
        global meeting_place

        view = Metting_time()
        meeting_place = "빅데이터실"
        await interaction.response.send_message(content= "회의할 시간을 선택해주세요", view=view)

    @discord.ui.button(label="컴플렉스존", style=discord.ButtonStyle.grey)
    async def metting_place_5(self, interaction:discord.Interaction, button : discord.ui.button):
        global meeting_place

        view = Metting_time()
        meeting_place = "컴플렉스존"
        await interaction.response.send_message(content= "회의할 시간을 선택해주세요", view=view)

    @discord.ui.button(label="기숙사 자습실", style=discord.ButtonStyle.grey)
    async def metting_place_6(self, interaction:discord.Interaction, button : discord.ui.button):
        global meeting_place

        view = Metting_time()
        meeting_place = "기숙사 자습실"
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
                if len(meeting_date) != 5 or meeting_date[2:3] != "-":
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

@tasks.loop(seconds=10)
async def every_hour_notice():
    channel = bot.get_channel(int(channel_url))

    if datetime.now().hour == 8 and datetime.now().minute == 00:
        await channel.send(content = "오늘의 회의 보고합니다!\n다들 오늘 하루도 화이팅하세요!", embed=embed)
        await channel.send("https://img.animalplanet.co.kr/news/2019/08/10/700/v4q0b0ff4hcpew1g6t39.jpg")
        time.sleep(1)
    
    for i in range(len(ref_get)-1):
        match ref_get[i+1].get('시간'):
            case '아침시간':
                if datetime.now().hour == 16 and datetime.now().minute == 23:
                    for i in range(len(ref_get)-1) :
                        print(ref_get[i+1].get('멤버'))
                        print("hello")
            case '점심시간':
                if datetime.now().hour == 13 and datetime.now().minute == 0:
                    await channel.send("점심시간 알림")
            case '저녁시간':
                if datetime.now().hour == 18 and datetime.now().minute == 0:
                    await channel.send("저녁시간 알림이야")
            case '7교시':
                if datetime.now().hour == 17 and datetime.now().minute == 52:
                    print(ref_get[i+1].get('멤버'))
                    for j in ref_get[i+1].get('멤버'):
                        print(j)
                        user_id = member_dict_get.get(j)
                        print(user_id)
                        user = bot.get_user(int(user_id))
                        print(user)
                        await user.send("테스트")
                    # for j in range(len(ref_get[i+1].get('멤버'))):
                    #     ref_get[j+1].get('멤버')
                        
            case '8교시':
                if datetime.now().hour == 16 and datetime.now().minute == 35:
                    await channel.send("10교시 알람이야!")
            case '9교시':
                if datetime.now().hour == 17 and datetime.now().minute == 25:
                    await channel.send("10교시 알람이야!")
            case '10교시':
                if datetime.now().hour == 14 and datetime.now().minute == 49:
                    await channel.send("10교시 알람이야!")
            case '11교시':
                if datetime.now().hour == 14 and datetime.now().minute == 51:
                    await channel.send("11교시 알람이야!")
            

        



bot.run(Token)