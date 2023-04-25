from meeting_time_select import Metting_time
from variable_manage import *

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