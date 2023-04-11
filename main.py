import discord
import os
import asyncio
import pytz

from discord.ext import commands
from dotenv import load_dotenv

from datetime import datetime

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
today_meet_count = 0
meeting_subject = ""
meeting_time = ""
meeting_place = ""

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
        global today_meet_count

        embed.add_field(name = meeting_subject, value = f"장소: {meeting_place}\n시간: {meeting_time}")
        today_meet_count += 1
        await interaction.response.send_message(content = "회의 등록이 완료되었어요!")

class Metting_time(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @discord.ui.button(label= "아침시간", style=discord.ButtonStyle.grey)
    async def metting_time_1(self, interaction:discord.Interaction, button:discord.ui.button):
        global meeting_time
        
        view = Metting_member()
        meeting_time = "아침시간"
        await interaction.response.send_message(content = "회의에 참석할 멤버를 선택해주세요.",view=view)

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
            await message.channel.send(content= "회의할 장소를 선택해주세요", view=view)



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