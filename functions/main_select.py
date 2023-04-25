from variable_manage import *
from functions.meeting_place_select import Metting_place


class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None


    @discord.ui.button(label="회의 신청", style=discord.ButtonStyle.grey)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        global meeting_subject
        global meeting_date

        view = Metting_place()
        member = interaction.user
        await interaction.response.send_message(content = "회의 주제를 알려주세요.")
        channel = bot.get_channel(int(channel_url))

        while(True):
            try:
                message = await bot.wait_for("message", check=lambda m: m.author == member and m.channel == channel, timeout=15.0)
            except asyncio.TimeoutError:
                await message.channel.send("15초가 지났어요. 명령어를 다시 실행시켜주세요.")
                break
        
            else :
                meeting_subject = message.content
                await message.channel.send(content= "회의할 날짜를 말해주세요. 이때 04-14 같은 형식으로 입력해주셔야해요!")
                try:
                    message = await bot.wait_for("message", check=lambda m: m.author == member and m.channel == channel, timeout=15.0)
                except asyncio.TimeoutError:
                    await message.channel.send("15초가 지났어요. 명령어를 다시 실행시켜주세요.")
                else:
                    meeting_date = message.content
                    if len(meeting_date) != 5 or meeting_date[2:3] != "-":
                        await message.channel.send("잘못된 정보를 입력하셨어요. 명령어를 다시 실행시켜주세요.")
                    else:   
                        await message.channel.send(content = "회의할 장소를 선택해주세요.", view=view)
                break



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