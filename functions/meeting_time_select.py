from variable_manage import *
from functions.meeting_member_selects import SelectPage1

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