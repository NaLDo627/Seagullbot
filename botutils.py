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


async def botutil_help(client, message):
    msg = '※ ()은 선택, <>은 필수입니다.\n'
    for i in range(0, len(HELP_LIST)):
        msg += '**' + HELP_LIST[i][0] + '**\n' + HELP_LIST[i][1] + '\n사용법: `' + HELP_LIST[i][2] + '`\n\n'
    embed = discord.Embed(description=msg,
                          color=0x00ff00)
    await message.channel.send('***ULTIMATE GUIDES for SEAGULLBOT***')
    await message.channel.send(embed=embed)


async def botutil_clear(client, message):
    def is_bot_command(m):
        return m.author == client.user or m.content.split(" ")[0] in COMMAND_LIST
    await message.channel.purge(limit=100, check=is_bot_command)


#ffmpeg 가 필요하며, ffmpeg 의 bin 폴더를 환경변수 설정해야 합니다.
async def botutil_reaction(argc, argv, client, message):
    # 먼저 이 함수가 호출되면 디렉토리를 스캔해서 리스트를 만든다
    # [190308][HKPARK] Default와 자신의 서버 ID의 폴더를 스캔한다. 이때 서버 ID의 폴더가 존재하지 않는다면 생성
    fid = None
    reaction_list = []

    if not (os.path.isdir(REACTION_DEFAULT_DIR)):
        os.makedirs(os.path.join(REACTION_DEFAULT_DIR))

    file_list = os.listdir(REACTION_DEFAULT_DIR)
    file_list.sort()
    for reaction in file_list:
        if ".mp3" in reaction:
            reaction_list.append(reaction.replace(".mp3", ""))

    music_path_dir = MUSIC_DIR_ID_FORMAT.format(message.guild.id)
    try:
        if not (os.path.isdir(music_path_dir)):
            os.makedirs(os.path.join(music_path_dir))
            filepath = os.path.join(music_path_dir, message.guild.name + ".txt")
            fid = open(filepath, "w")
            if not os.path.isfile(filepath):
                fid.write(message.guild.name)

    except OSError as e:
        print('ERROR: ' + str(e))
    finally:
        if fid is not None:
            fid.close()

    file_list = os.listdir(music_path_dir)
    file_list.sort()
    for reaction in file_list:
        if ".mp3" in reaction:
            reaction_list.append(reaction.replace(".mp3", ""))

    # 중복제거
    reaction_list = list(set(reaction_list))
    reaction_list.sort()

    # Step 1. 파라미터 갯수 체크
    if argc == 1:
        embed = discord.Embed(title='!리액션 (커맨드)로 리액션을 재생할 수 있습니다.',
                              description='*커맨드 목록*\n```' + str(reaction_list) + '```',
                              color=0xfdee00)
        await message.channel.send(embed=embed)
        return

    # Step 2. 유효한 커맨드인지 체크
    command = argv[1]
    if command not in reaction_list:
        embed = discord.Embed(title='존재하지 않는 커맨드입니다.',
                              description='*커맨드 목록*\n```' + str(reaction_list) + '```',
                              color=0xfdee00)
        await message.channel.send(embed=embed)
        return

    # Step 3. 사용자가 음성채팅에 접속해 있는지 체크
    author = message.author
    voice_state = author.voice
    if voice_state is None:
        await message.channel.send('음성 채팅에 접속해야 이용할 수 있습니다.', delete_after=10)
        return

    # # Step 4. 이미 재생중인지 체크
    # if client.user.voice is not None:
    #     await message.channel.send('현재 재생이 끝난 후 사용해 주세요.2', delete_after=10)
    #     return

    voice_client = None
    try:
        # [190308][HKPARK] 경로 검사를 먼저 해봐야함; 이게 Default에 있는 음악파일인지 서버 폴더에 있는 파일인지
        # 만약 둘 다 파일명이 존재하면 서버 폴더 우선
        # voice = await client.join_voice_channel(channel)
        voice_channel = voice_state.channel
        voice_client = await voice_channel.connect()
        music_path = "{}/{}.mp3".format(music_path_dir, command) if os.path.exists("{}/{}.mp3".format(music_path_dir, command)) \
                                                            else "{}/{}.mp3".format(REACTION_DEFAULT_DIR, command)
        #player = voice.create_ffmpeg_player(music_path, options=" -af 'volume=0.3'")
        ffmpeg_player = discord.FFmpegPCMAudio(music_path, options=" -af 'volume=0.3'")
        voice_client.play(ffmpeg_player)
        # player.start()
        while voice_client.is_playing():
            await asyncio.sleep(1)
        # disconnect after the player has finished
        voice_client.stop()
    except discord.ClientException as ex:
        print(ex.args[0])
        if ex.args[0] == "ffmpeg was not found.":
            await message.channel.send('FFMPEG가 설치되어 있지 않습니다.', delete_after=10)
        elif ex.args[0] == "Already connected to a voice channel.":
            await message.channel.send('현재 재생이 끝난 후 사용해 주세요.', delete_after=10)
        else:
            await message.channel.send('알 수 없는 오류로 인해 재생이 불가합니다.', delete_after=10)
    except Exception as ex:
        print(ex)
    finally:
        if voice_client is not None:
            await voice_client.disconnect()


async def botutil_vote(argc, argv, client, message):
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


async def botutil_team(argc, argv, client, message):
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


async def botutil_jebi(argc, argv, client, message):
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

## TODO: 봇조종 방법 개선 및 사용 채널 세분화
async def botutil_botctl(argc, argv, client, message):
    if argc != 3:
        await message.channel.send(message.channel, '타겟 설정이 잘못되었습니다. 다시 해주세요.')
        return

    botctl_dic = {}
    if os.path.exists('./botctl.json'):
        with open('botctl.json') as json_file:
            botctl_dic = json.load(json_file)

    botctl_dic[message.author.id] = [argv[1], argv[2]]

    with open('botctl.json', 'w') as new_file:
        json.dump(botctl_dic, new_file, ensure_ascii=False, indent='\t')

    await message.channel.send('타겟 설정 완료, 서버 ID: {}, 채널 ID: {}'.format(argv[1], argv[2]))


async def botutil_botsay(argc, argv, client, message):
    botctl_dic = {}
    if not os.path.exists('./botctl.json'):
        await message.channel.send('먼저 타겟을 설정해야 합니다.')
        return

    with open('botctl.json') as json_file:
        botctl_dic = json.load(json_file)

    if str(message.author.id) not in botctl_dic.keys():
        # !봇조종 <서버ID> <채널ID>
        await message.channel.send('먼저 타겟을 설정해야 합니다.')
        return
    try:
        target_channel = client.get_channel(int(botctl_dic[str(message.author.id)][1]))
        if target_channel is None:
            await message.channel.send('타겟이 잘못되었습니다. 재설정 해주세요.')
            return

        await target_channel.send(message.content[message.content.find(' ')+1:])
    except Exception as ex:
        print(ex)
        await message.channel.send('봇말 사용에서 오류가 발생했습니다. 사실 아직 잘 안돼요ㅎㅎ;')
        return


async def botutil_reaction_upload(argc, argv, client, message):
    def is_caller(m):
        return m.author == message.author

    music_path = MUSIC_DIR_ID_FORMAT.format(message.guild.id)
    uploadplz = await message.channel.send('리액션 mp3를 업로드 하세요.')
    msg = await client.wait_for("message", timeout=60.0, check=is_caller)
    await uploadplz.delete()

    if msg is None or len(msg.attachments) == 0:
        await message.channel.send('업로드된 파일이 없습니다.', delete_after=10)
        if msg is not None:
            await msg.delete()
        return

    url = msg.attachments[0].url
    if url is None or url[-4:] != '.mp3':
        await message.channel.send('mp3 파일을 업로드 해주세요!', delete_after=10)
        await msg.delete()
        return

    file_name = msg.content
    if file_name is None or len(file_name) == 0:
        file_name = msg.attachments[0].filename.replace('.mp3', '')

    # 업로드 전 해당 파일명이 있는지 검사
    if os.path.exists(music_path+'/'+file_name+'.mp3'):
        await message.channel.send('이미 존재하는 파일명입니다.')
        await msg.delete()
        return

    uploading = await message.channel.send('업로드 중..')
    await download_mp3_file(url, music_path, file_name)
    await msg.delete()
    await uploading.edit(content='업로드가 완료되었습니다.')


async def download_mp3_file(url, path, file_name):
    if not os.path.exists(path):
        os.makedirs(path)
    headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'
    }
    r = requests.get(url, headers=headers, stream=True)
    with open(path+'/'+str(file_name)+'.mp3', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
