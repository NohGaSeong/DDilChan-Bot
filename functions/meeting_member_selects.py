from variable_manage import *

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