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

###### 디스코드 봇 관련 설정 ######
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
allowed_mentions = discord.AllowedMentions(everyone = True)

###### .env 관련 변수 ######
load_dotenv()
Token = os.getenv('Token')
database_url = os.getenv('database_url')
guild_url = os.getenv('guild_url')
channel_url = os.getenv('channel_url')
many_many_meeting_vichan_gif = ('many_many_meeting_vichan_gif')
many_meeting_vichan_gif = os.getenv('many_meeting_vichan_gif')
one_meeting_vichan_gif = os.getenv('one_meeting_vichan_gif')
no_meeting_vichan_gif = os.getenv('no_meeting_vichan_gif')

###### 기본적으로 사용하는 변수 선언 ######
today_meet_count = 0
db_count = 0

meeting_subject = ""
meeting_time = ""
meeting_place = ""
meeting_member = []
meeting_member_check = []
meeting_date = ""

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