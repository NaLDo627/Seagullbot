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
import random


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


async def divide_by_team(argc, argv, client, message):
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
            await message.channel.send('입력받은 시간 초과입니다.')
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
            await message.channel.send('입력받은 시간 초과입니다.')
            return
        party_string = msg.content
        await msg.delete()
    else:
        party_string = argv[3]

    party_list = party_string.split(',')

    if len(party_list) <= jebi_count:
        await message.channel.send('뽑을 사람수와 참여하는 사람수를 확인해주세요.')
        return

    jebi_list = []
    for i in range(0, jebi_count):
        jebi_target = random.choice(party_list)
        jebi_list.append(jebi_target)
        party_list.remove(jebi_target)
    await message.channel.send('뽑힌사람은.. ')
    await asyncio.sleep(1)
    await message.channel.send(str(jebi_list).replace(" ", "") + '!')
