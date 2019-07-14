import discord
import asyncio
from constant import *
import os
import json
import requests


# 명령어를 사용한 사람이 채널 관리 권한을 가지고 있는 지 확인한다.
def admin_only(command_func):
    #def check_admin_role(message_author, channel):
    async def check_admin_role(*args, **kwargs):
        #guild_permissions = message_author.guild_permissions
        guild_permissions = args[3].author.permissions_in(args[3].channel)
        if not guild_permissions.manage_guild:
            await args[3].channel.send('이 명령어에 대한 권한이 없습니다.')
            return
        return await command_func(*args, **kwargs)
    return check_admin_role


## TODO: 봇조종 방법 개선 및 사용 채널 세분화
@admin_only
async def set_target_channel_to_say(argc, argv, client, message):
    if argc != 3:
        await message.channel.send('타겟 설정이 잘못되었습니다. 다시 해주세요.')
        return

    botctl_dic = {}
    if os.path.exists('./botctl.json'):
        with open('botctl.json') as json_file:
            botctl_dic = json.load(json_file)

    botctl_dic[message.author.id] = [argv[1], argv[2]]

    with open('botctl.json', 'w') as new_file:
        json.dump(botctl_dic, new_file, ensure_ascii=False, indent='\t')

    await message.channel.send('타겟 설정 완료, 서버 ID: {}, 채널 ID: {}'.format(argv[1], argv[2]))

@admin_only
async def say_bot_to_channel(argc, argv, client, message):
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

@admin_only
async def upload_reaction(argc, argv, client, message):
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



