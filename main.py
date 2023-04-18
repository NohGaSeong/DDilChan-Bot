import discord
import os
import asyncio
import pytz
import time 
import firebase_admin
import json

from discord.ext import commands, tasks
from dotenv import load_dotenv
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime,date


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

###### 기본적으로 사용하는 변수 선언 ######
today_meet_count = 0
db_count = 0

meeting_subject = ""
meeting_time = ""
meeting_place = ""
meeting_member = []
meeting_member_check = []


###### .env 관련 변수 ######
load_dotenv()
Token = os.getenv('Token')
database_url = os.getenv('database_url')
guild_url = os.getenv('guild_url')
channel_url = os.getenv('channel_url')
many_many_metting_vichan_gif = "https://cdn.discordapp.com/attachments/953156775262167111/1095244923550302208/WASTED.png"
many_metting_vichan_gif = os.getenv('many_metting_vichan_gif')
one_metting_vichan_gif = os.getenv('one_metting_vichan_gif')
no_metting_vichan_gif = os.getenv('no_metting_vichan_gif')

###### 봇 임베드 추가 ######
embed=discord.Embed(timestamp=datetime.now(pytz.timezone('UTC')), color=0x54b800)

###### 파이어베이스 연동 관련 코드 ######
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

###### json 관련 코드 ######
with open('member_list_1.json', 'r') as f:
    json_member_1 = json.load(f)

with open('member_list_2.json', 'r') as f:
    json_member_2 = json.load(f)

options_count = 0
options_count_2 = 0
options = []
options_2 = []

for key, val in json_member_1.items():
    options_count += 1
    options.append(discord.SelectOption(label=key, description=val))

for key, val in json_member_2.items():
    options_count_2 += 1
    options_2.append(discord.SelectOption(label=key, description=val))

####### bot 시작 ######
@bot.event
async def on_ready():
    global today_meet_count
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')
    print(Token)
    print(member_dict_get)
    print(options_count_2)
    active = discord.Game("!띨챤 으로 회의준비")
    await bot.change_presence(status=discord.Status.idle, activity=active)

    for i in range(len(ref_get)-1):
        embed.add_field(name=f"{ref_get[i+1].get('주제')}", 
                        value = f"날짜 : {ref_get[i+1].get('날짜')}\n"
                            + f"회의시간: {ref_get[i+1].get('시간')}\n"
                            + f"회의장소: {ref_get[i+1].get('장소')}\n"
                            + f"참석인원: {ref_get[i+1].get('멤버')}\n",
                        inline=False)
        today_meet_count += 1

    every_hour_notice.start()

###### !챤하 ######
@bot.command()
async def 챤하(ctx):
    view = Menu()
    await ctx.reply("챤하 ~ 무엇을 도와드릴까요?", view=view)

###### 회의 인원 선택 ######
class SelectPage1(discord.ui.View):
    @discord.ui.select(
            placeholder = "회의 멤버를 선택해주세요.",
            min_values = 1,
            max_values = options_count,
            options=options
            )
    async def select_callback(self, select, interaction):
        global db_count
        global meeting_member

        meeting_member = interaction.values


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

class SelectPage2(discord.ui.View):
    @discord.ui.select(
            placeholder = "회의 멤버를 선택해주세요.",
            min_values = 1,
            max_values = options_count_2,
            options=options_2
        )

    async def select_callback(self, select, interaction):
        global db_count
        global meeting_member

        meeting_member += interaction.values
        meeting_member.remove("다음페이지")
        
        db_count += 1
        ref =  db.reference(meeting_date + "/" + str(db_count))
        ref.update({'주제': str(meeting_subject)})
        ref.update({'날짜': str(meeting_date)})
        ref.update({'시간': meeting_time})
        ref.update({'장소': meeting_place})
        ref.update({'멤버': meeting_member})
        await select.response.send_message("회의 등록이 완료됐어요.")

###### 회의 시간 선택 ######
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

###### 회의 장소 선택 ######
class Metting_place(discord.ui.View):
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

###### 회의 알림 View ######
class Meeting_check(discord.ui.View):
    @discord.ui.select(
        placeholder = "호출 멤버를 선택해주세요.",
        min_values = 1,
        max_values = options_count,
        options=options
        )

    async def select_callback(self, select, interaction):
        global meeting_member

        meeting_member = interaction.values

        if "다음페이지" in interaction.values:
            view = Meeting_check_2()
            await select.response.send_message(content = "회의에 호출할 멤버를 선택해주세요.", view=view)
        else :
            for i in meeting_member:
                # user_id = member_dict_get.get(j)
                # user = bot.get_user(int(user_id))
                print(i)
            await select.response.send_message("회의 호출이 완료되었어요.")

class Meeting_check_2(discord.ui.View):
    @discord.ui.select(
            placeholder = "호출 멤버를 선택해주세요.",
            min_values = 1,
            max_values = options_count_2,
            options=options_2
        )

    async def select_callback(self, select, interaction):
        global meeting_member

        meeting_member += interaction.values
        meeting_member.remove("다음페이지")

        for i in meeting_member:
            user_id = member_dict_get.get(i)
            user = bot.get_user(int(user_id))
            await user.send("회의 빨리와용")    
        
        await select.response.send_message("회의 호출이 완료되었어요.")
    





###### !챤하's View ######
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
    
    @discord.ui.button(label="이슈보고 및 깃허브", style = discord.ButtonStyle.red)
    async def menu3(self, interaction: discord.Interaction, button : discord.ui.Button):
        await interaction.response.send_message("디스코드:가성#7216\n깃허브:NohGaSeong/DDilChan-Bot\n로 이슈 제보 및 코드 리뷰 부탁드려요!")

###### 백그라운드 함수 ######
@tasks.loop(seconds=20)
async def every_hour_notice():
    channel = bot.get_channel(int(channel_url))

    if datetime.now().hour == 8 and datetime.now().minute == 0:
        await channel.send(content = "오늘의 회의 보고합니다!\n다들 오늘 하루도 화이팅하세요!", embed=embed)
        await channel.send("https://img.animalplanet.co.kr/news/2019/08/10/700/v4q0b0ff4hcpew1g6t39.jpg")
        time.sleep(1)
    
    for i in range(len(ref_get)-1): 
        ###### 이슈로 인해 추후 코드 최적화 예정 ######
        for j in ref_get[i+1].get('멤버') :
            user_id = member_dict_get.get(j)
            user = bot.get_user(int(user_id))
            view = Meeting_check()

        match ref_get[i+1].get('시간'):
            case '아침시간':
                if datetime.now().hour == 17 and datetime.now().minute == 12:
                    await user.send(content = "5분 뒤 회의!\n오늘의 회의 목록을 보고 장소를 참고해주세요!", embed=embed)
                if datetime.now().hour == 17 and datetime.now().minute == 24:
                    await channel.send(content = "회의 시작해요! 멤버 호출 하실래요?", view=view)
            case '점심시간':
                if datetime.now().hour == 12 and datetime.now().minute == 55:
                    await user.send(content = "5분 뒤 회의!\n오늘의 회의 목록을 보고 장소를 참고해주세요!", embed=embed)
                if datetime.now().hour == 13 and datetime.now().minute == 0:
                    await channel.send(content = "회의 시작해요! 멤버 호출 하실래요?", view=view)
            case '저녁시간':
                if datetime.now().hour == 17 and datetime.now().minute == 55:
                    await user.send(content = "5분 뒤 회의!\n오늘의 회의 목록을 보고 장소를 참고해주세요!", embed=embed)
                if datetime.now().hour == 13 and datetime.now().minute == 0:
                    await channel.send(content = "회의 시작해요! 멤버 호출 하실래요?", view=view)
            case '7교시':
                if datetime.now().hour == 15 and datetime.now().minute == 25:
                    await user.send(content = "5분 뒤 회의!\n오늘의 회의 목록을 보고 장소를 참고해주세요!", embed=embed)
                if datetime.now().hour == 15 and datetime.now().minute == 30:
                    await channel.send(content = "회의 시작해요! 멤버 호출 하실래요?", view=view)
            case '8교시':
                if datetime.now().hour == 16 and datetime.now().minute == 35:
                    await user.send(content = "5분 뒤 회의!\n오늘의 회의 목록을 보고 장소를 참고해주세요!", embed=embed)
                if datetime.now().hour == 16 and datetime.now().minute == 40:
                    await channel.send(content = "회의 시작해요! 멤버 호출 하실래요?", view=view)
            case '9교시':
                if datetime.now().hour == 17 and datetime.now().minute == 25:
                    await user.send(content = "5분 뒤 회의!\n오늘의 회의 목록을 보고 장소를 참고해주세요!", embed=embed)
                if datetime.now().hour == 17 and datetime.now().minute == 30:
                    await channel.send(content = "회의 시작해요! 멤버 호출 하실래요?", view=view)
            case '10교시':
                if datetime.now().hour == 19 and datetime.now().minute == 25:
                        await user.send(content = "5분 뒤 회의!\n오늘의 회의 목록을 보고 장소를 참고해주세요!", embed=embed)
                if datetime.now().hour == 19 and datetime.now().minute == 30:
                    await channel.send(content = "회의 시작해요! 멤버 호출 하실래요?", view=view)
            case '11교시':
                if datetime.now().hour == 20 and datetime.now().minute == 25:
                        await user.send(content = "5분 뒤 회의!\n오늘의 회의 목록을 보고 장소를 참고해주세요!", embed=embed)
                if datetime.now().hour == 20 and datetime.now().minute == 30:
                    await channel.send(content = "회의 시작해요! 멤버 호출 하실래요?", view=view)
        


###### 봇 구동 ######
bot.run(Token)