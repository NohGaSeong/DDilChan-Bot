from functions.main_select import Menu
from functions.meeting_takepart import Meeting_opinion_button
from variable_manage import *
import variable_manage as var_manage

####### bot 시작 ######
@bot.event
async def on_ready():
    global today_meet_count
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')
    print(Token)
    active = discord.Game("!띨챤 으로 회의준비")
    await bot.change_presence(status=discord.Status.idle, activity=active)
    
    try:
        for i in range(len(ref_get)-1):
            var_manage.embed.add_field(name=f"{ref_get[i+1].get('주제')}", 
                            value = f"날짜 : {ref_get[i+1].get('날짜')}\n"
                                + f"회의시간: {ref_get[i+1].get('시간')}\n"
                                + f"회의장소: {ref_get[i+1].get('장소')}\n"
                                + f"참석인원: {ref_get[i+1].get('멤버')}\n",
                            inline=False)
            var_manage.today_meet_count += 1
    except:
        print("오늘은 회의가 없어용")

    every_hour_notice.start()

###### !챤하 ######
@bot.command()
async def 챤하(ctx):
    view = Menu()
    await ctx.reply("챤하 ~ 무엇을 도와드릴까요?", view=view)


###### 백그라운드 함수 ######
@tasks.loop(seconds=20)
async def every_hour_notice():
    channel = bot.get_channel(int(channel_url))
    if datetime.now().hour == 8 and datetime.now().minute == 0:
        embed.add_field(name="오늘의 회의", value = "아래의 회의들을 보고 참고해주세요!\n\n")
        await channel.send(content = "@everywone 오늘의 회의 보고합니다!\n다들 오늘 하루도 화이팅하세요!", embed=embed, allowed_mentions = allowed_mentions)
        await channel.send("https://img.animalplanet.co.kr/news/2019/08/10/700/v4q0b0ff4hcpew1g6t39.jpg")
        time.sleep(1)
    
    try:
        for i in range(len(ref_get)-1): 
            ###### 이슈로 인해 추후 코드 최적화 예정 ######
            for j in ref_get[i+1].get('멤버') :
                user_id = member_dict_get.get(j)
                user = bot.get_user(int(user_id))
                view = Meeting_opinion_button

                match ref_get[i+1].get('시간'):
                    case '아침시간':
                        if datetime.now().hour == 7 and datetime.now().minute == 55:
                            await user.send(content = "5분 뒤 회의!\n오늘의 회의 목록을 보고 장소를 참고해주세요!", embed=embed)
                        if datetime.now().hour == 8 and datetime.now().minute == 0:
                            await channel.send(content = "회의 시작해요! 멤버 호출 하실래요?", view=view)
                    case '점심시간':
                        if datetime.now().hour == 12 and datetime.now().minute == 55:
                            await user.send(content = "5분 뒤 회의!\n오늘의 회의 목록을 보고 장소를 참고해주세요!", embed=embed)
                        if datetime.now().hour == 13 and datetime.now().minute == 0:
                            await channel.send(content = "회의 시작해요! 멤버 호출 하실래요?", view=view)
                    case '저녁시간':
                        if datetime.now().hour == 17 and datetime.now().minute == 55:
                            await user.send(content = "5분 뒤 회의!\n오늘의 회의 목록을 보고 장소를 참고해주세요!", embed=embed)
                        if datetime.now().hour == 18 and datetime.now().minute == 0:
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
    except:
        print("오늘 회의 없어용")


###### 봇 구동 ######
bot.run(Token)