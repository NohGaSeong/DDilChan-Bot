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


@bot.command()
async def 챤하(ctx):
    view = Menu()
    await ctx.reply("챤하 ~ 무엇을 도와드릴까요?", view=view)

# class FavouriteGameSelect(discord.ui.Select):
#     def __init__(self):
#         options = [ 
#             discord.SelectOption(label="Cs", value="cs"),
#             discord.SelectOption(label="Minecraft", value="mc"),
#             discord.SelectOption(label="Fortnite", value="f"),
#         ]
#         super().__init__(options=options, placeholder="What do you like to play?", max_values=2)

#     async def callback(self, interaction:discord.Interaction):
#         await self.view.respond_to_answer2(interaction, self.values)

# class ServeyView(discord.ui.View):
#     answer1 = None
#     answer2 = None

#     @discord.ui.select(
#         placeholder="회의 인원을 선택해주세요!",
#         options=[
#         discord.SelectOption(label="이현빈", description="안드로이드", emoji="🤖"),
#         discord.SelectOption(label="김현승", description="안드로이드", emoji="🤖"),
#         discord.SelectOption(label="백승민", description="안드로이드", emoji="🤖")
#         ]
#     )

#     async def select_age(self, interaction:discord.Interaction, select_item : discord.ui.Select):
#         self.answer1 = select_item.values
#         self.children[0].disabled= True
#         game_select = FavouriteGameSelect()
#         self.add_item(game_select)
#         await interaction.message.edit(view=self)
#         await interaction.response.defer()

#     async def respond_to_answer2(self, interaction : discord.Interaction, choices):
#         self.answer2 = choices 
#         self.children[1].disabled= True
#         await interaction.message.edit(view=self)
#         await interaction.response.defer()
#         self.stop()


# class Member_select(discord.ui.View):
#     def __init__(self):
#         super().__init()
#         self.value = None
    
#     @discord.ui.select(
#         placeholder="hi",
#         options = [
#             discord.SelectOption(label="1", value ="1"),
#             discord.SelectOption(label="2", value ="2"),
#             discord.SelectOption(label="3", value ="3")
#         ],
#         min_values = 2,
#         max_values = 3,
#         row = 2
#     )

#     async def callback(interaction:discord.Interaction):
#         await interaction.response.send_message("Hello World!")


class SelectPage2(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.select(
            min_values = 1,
            max_values = 3,
            placeholder = "Choose",
            options = [
                discord.SelectOption(
                    label="승민",
                    emoji="😀",
                    description="안드로이드"
                ),
                discord.SelectOption(
                    label="현빈",
                    emoji="😀",
                    description="안드로이드"
                ),
                discord.SelectOption(
                    label="현승",
                    emoji="😀",
                    description="안드로이드"
                ),
            ],
            row = 2
        )

    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        await select.response.send_message("회의 등록이 완료되었어요.")

    
class SelectPage1(discord.ui.View):
    @discord.ui.select(
            placeholder = "Choose",
            min_values = 1,
            max_values = 4,
            options = [
                discord.SelectOption(
                    label="승민",
                    emoji="😀",
                    description="안드로이드"
                ),
                discord.SelectOption(
                    label="현빈",
                    emoji="😀",
                    description="안드로이드"
                ),
                discord.SelectOption(
                    label="현승",
                    emoji="😀",
                    description="안드로이드"
                ),
                discord.SelectOption(
                    label="다음 페이지",
                    emoji="😀",
                    description="다음 페이지"
                )
            ]
        )
    async def select_callback(self, select, interaction):
        if "다음 페이지" in interaction.values:
            view = SelectPage2()
            await select.response.send_message(content = "회의에 참석할 멤버를 선택해주세요.", view=view)
        else :
            await select.response.send_message("회의 등록이 완료되었어요.")

        

class Metting_time(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label= "아침시간", style=discord.ButtonStyle.grey)
    async def metting_time_1(self, interaction:discord.Interaction, button:discord.ui.button):
        view = SelectPage1()
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




bot.run(Token)