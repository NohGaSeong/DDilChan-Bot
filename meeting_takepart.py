from variable_manage import *

class Meeting_opinion_button(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="참가했는뎁요..?", style=discord.ButtonStyle.grey)
    async def opinion_button_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = bot.get_channel(int(channel_url))
        await interaction.response.send_message(content = "장난치지말라고 전해줄게요!")
        await channel.send(f"{interaction.user} 님에게 장난치지마세요!")
    
    @discord.ui.button(label="가고 있어요!", style=discord.ButtonStyle.grey)
    async def opinion_button_2(self, interaction: discord.Interaction, button : discord.ui.Button):
        channel = bot.get_channel(int(channel_url))
        await interaction.response.send_message(content = "빨리 와주세요!")
        await channel.send(f"{interaction.user} 님은 가고 있어요 라고 반응하셨어요!")
    
    @discord.ui.button(label="불참이에요.", style=discord.ButtonStyle.red)
    async def opinion_button_3(self, interaction: discord.Interaction, button : discord.ui.Button):
        channel = bot.get_channel(int(channel_url))
        await interaction.response.send_message(content = "다음부턴 미리 말해주세요...!")
        await channel.send(f"{interaction.user} 님은 불참이라고 반응하셨어요!")