from variable_manage import *
from meeting_takepart import Meeting_opinion_button

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
                user_id = member_dict_get.get(i)
                user = bot.get_user(int(user_id))
                await user.send(content = "회의 빨리와용", view = Meeting_opinion_button()) 
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
        view = Meeting_opinion_button()

        for i in meeting_member:
            user_id = member_dict_get.get(i)
            user = bot.get_user(int(user_id))
            await user.send(content = "회의 빨리와용", view = view)    
        
        await select.response.send_message("회의 호출이 완료되었어요.")