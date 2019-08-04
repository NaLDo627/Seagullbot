import urllib.request
from bs4 import BeautifulSoup
import json
import requests
import discord
import asyncio
import prettytable
from selenium import webdriver
import datetime
from constant import *
import os
from datetime import datetime
import random
from ..utils import _get


async def show_help(client, message):
    msg = '※ ()은 선택, <>은 필수입니다.\n'
    for i in range(0, len(HELP_LIST)):
        msg += '**' + HELP_LIST[i][0] + '**\n' + HELP_LIST[i][1] + '\n사용법: `' + HELP_LIST[i][2] + '`\n\n'
    embed = discord.Embed(description=msg,
                          color=0x00ff00)
    await message.channel.send('***ULTIMATE GUIDES for SEAGULLBOT***')
    await message.channel.send(embed=embed)


async def clear_command(client, message):
    def is_bot_command(m):
        return m.author == client.user or m.content.split(" ")[0] in COMMAND_LIST
    await message.channel.purge(limit=100, check=is_bot_command)


async def vote_by_reaction(argc, argv, client, message):
    if argc == 1:
        time = 30
    else:
        time = int(argv[1])

    msg = await message.channel.send('투표하세요! 시간제한: *' + str(time) + '초*')
    reactions = ['👍', '👎']
    for emoji in reactions:
        await msg.add_reaction(emoji)
    await asyncio.sleep(time)

    cache_msg = discord.utils.get(client.cached_messages, id=msg.id)
    for reaction in cache_msg.reactions:
        async for user in reaction.users():
            if user.id != client.user.id:
                await message.channel.send('{0} has reacted with {1.emoji}!'.format(user.name, reaction))
        #reactors = await client.get_reaction_users(reactor)

        # # from here you can do whatever you need with the member objects
        # for member in reactors:
        #     if member.id != client.user.id:
        #         await message.channel.send(member.name)


async def divide_team_by_text(argc, argv, client, message):
    if argc == 1:
        team_count = 2
    else:
        team_count = int(argv[1])

    if team_count < 2:
        await message.channel.send('팀 수는 2 이상 가능합니다.', delete_after=10)
        return

    team_no = []

    for i in range(0, team_count):
        team_no.append([])

    if argc <= 2:
        def is_caller(m):
            return m.author == message.author

        party = await message.channel.send('참여원을 콤마(,)로 구분지어서 적어주세요.(제한시간 1분)')
        msg = await client.wait_for("message", timeout=60.0, check=is_caller)
        await party.delete()
        if msg is None:
            await message.channel.send('입력받은 시간 초과입니다.', delete_after=10)
            return
        party_string = msg.content
        await msg.delete()
    else:
        party_string = argv[3]

    party_list = party_string.split(',')
    team_member_count = int(len(party_list) / team_count)

    for i in range(0, team_count):
        for j in range(0, team_member_count):
            random_member = random.choice(party_list)
            team_no[i].append(random_member)
            party_list.remove(random_member)

    if len(party_list) is not 0:
        index = 0
        while len(party_list) is not 0:
            team_no[index % team_count].append(party_list[0])
            party_list.remove(party_list[0])
            index += 1

    await message.channel.send('팀 나누기 결과 : \n')
    result_msg = ''
    for i in range(0, team_count):
        result_msg += '팀 ' + str(i + 1) + ': ' + str(team_no[i]).replace(' ', '') + '\n'

    await message.channel.send(result_msg)


async def divide_team_by_voice_channel(argc, argv, client, message):
    if argc == 1:
        team_count = 2
    else:
        team_count = int(argv[1])

    if team_count < 2:
        await message.channel.send('팀 수는 2 이상 가능합니다.', delete_after=10)
        return

    team_no = []

    for i in range(0, team_count):
        team_no.append([])

    # Step 1. 메세지 작성자가 음성채널에 있는지 검사
    author = message.author
    voice_state = author.voice
    if voice_state is None:
        await message.channel.send('음성 채팅에 접속해야 이용할 수 있습니다.', delete_after=10)
        return

    # Step 2. 메세지 작성자가 포함되어 있는 음성채널의 멤버들을 추출
    voice_channel = voice_state.channel
    voice_members = voice_channel.members

    # Step 3. 봇은 제외하고 리스트에 추가한다.
    party_list = []
    for voice_member in voice_members:
        if not voice_member.bot:
            party_list.append(voice_member.name)

    team_member_count = int(len(party_list) / team_count)

    for i in range(0, team_count):
        for j in range(0, team_member_count):
            random_member = random.choice(party_list)
            team_no[i].append(random_member)
            party_list.remove(random_member)

    if len(party_list) is not 0:
        index = 0
        while len(party_list) is not 0:
            team_no[index % team_count].append(party_list[0])
            party_list.remove(party_list[0])
            index += 1

    await message.channel.send('팀 나누기 결과 : \n')
    result_msg = ''
    for i in range(0, team_count):
        result_msg += '팀 ' + str(i + 1) + ': ' + str(team_no[i]).replace(' ', '') + '\n'

    await message.channel.send(result_msg)


async def lottery(argc, argv, client, message):
    jebi_count = 0
    if argc == 1:
        jebi_count = 1
    else:
        jebi_count = int(argv[1])

    party_string = ''
    if argc <= 2:
        team_no = []

        def is_caller(m):
            return m.author == message.author

        party = await message.channel.send('참여원을 콤마(,)로 구분지어서 적어주세요.(제한시간 1분)')
        msg = await client.wait_for("message", timeout=60.0, check=is_caller)
        await party.delete()
        if msg is None:
            await message.channel.send('입력받은 시간 초과입니다.', delete_after=10)
            return
        party_string = msg.content
        await msg.delete()
    else:
        party_string = argv[3]

    party_list = party_string.split(',')

    if len(party_list) <= jebi_count:
        await message.channel.send('뽑을 사람수와 참여하는 사람수를 확인해주세요.', delete_after=10)
        return

    jebi_list = []
    for i in range(0, jebi_count):
        jebi_target = random.choice(party_list)
        jebi_list.append(jebi_target)
        party_list.remove(jebi_target)
    await message.channel.send('뽑힌사람은.. ')
    await asyncio.sleep(1)
    await message.channel.send(str(jebi_list).replace(" ", "") + '!')


async def replay_ui_pubg(argc, argv, client, message):
    def is_caller(m):
        return m.author == message.author

    if argc == 1:
        searching = await message.channel.send('아이디를 입력하세요.')
        msg = await client.wait_for("message", timeout=15.0, check=is_caller)
        if msg is None:
            await searching.delete()
            await message.channel.send('입력받은 시간 초과입니다.', delete_after=10)
            return

        player_id = msg.content
        await msg.delete()

        if player_id is None:
            await searching.delete()
            await message.channel.send('입력받은 아이디가 없습니다.', delete_after=10)
            return
        await searching.edit(content='검색중입니다..')
    else:
        player_id = argv[1]
        searching = await message.channel.send('검색중입니다..')

    res = _get("http://ec2-15-164-104-223.ap-northeast-2.compute.amazonaws.com:10000/api/pubg/matches/" + player_id)

    if res['error']:
        result = '플레이어를 찾을 수 없습니다.'
        await message.channel.send(result, delete_after=10)
        await searching.delete()
        return

    await message.channel.trigger_typing()
    replays = ""
    for i, content in enumerate(res['content']):
        if i > 9:
            break
        replays += "[{}](http://ec2-15-164-104-223.ap-northeast-2.compute.amazonaws.com:12000/pubg/{}/steam/{})\n".\
            format(content['createdAt'], player_id, content['id'])

    embed = discord.Embed(title='현재 재생가능한 PUBG Replay들',
                          description=replays,
                          color=0x879396)
    await message.channel.send(embed=embed)
    await searching.delete()

async def replay_ui_lol(argc, argv, client, message):
    def is_caller(m):
        return m.author == message.author

    if argc == 1:
        searching = await message.channel.send('아이디를 입력하세요.')
        msg = await client.wait_for("message", timeout=15.0, check=is_caller)
        if msg is None:
            await searching.delete()
            await message.channel.send('입력받은 시간 초과입니다.', delete_after=10)
            return

        player_id = msg.content
        await msg.delete()

        if player_id is None:
            await searching.delete()
            await message.channel.send('입력받은 아이디가 없습니다.', delete_after=10)
            return
        await searching.edit(content='검색중입니다..')
    else:
        player_id = argv[1]
        searching = await message.channel.send('검색중입니다..')

    res = _get("http://ec2-15-164-104-223.ap-northeast-2.compute.amazonaws.com:10000/api/lol/matches/" + player_id)

    if res['error']:
        result = '플레이어를 찾을 수 없습니다.'
        await message.channel.send(result, delete_after=10)
        await searching.delete()
        return

    await message.channel.trigger_typing()
    replays = ""
    for i, content in enumerate(res['content']['matches']):
        if i > 9:
            break
        replays += "[{}](http://ec2-15-164-104-223.ap-northeast-2.compute.amazonaws.com:12000/lol/{}/kr/{})\n". \
            format(datetime.fromtimestamp(content['timestamp']/1000).strftime("%Y-%m-%d %H:%M:%S"), player_id, content['gameId'])

    embed = discord.Embed(title='현재 재생가능한 LOL Replay들',
                          description=replays,
                          color=0x879396)
    await message.channel.send(embed=embed)
    await searching.delete()

