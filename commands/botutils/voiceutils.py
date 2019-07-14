import discord
import asyncio
from constant import *
import os


#ffmpeg 가 필요하며, ffmpeg 의 bin 폴더를 환경변수 설정해야 합니다.
async def play_reaction(argc, argv, client, message):
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


async def stop_playing(argc, argv, client, message):
    # Step 1. 사용자가 음성채팅에 접속해 있는지 체크
    author = message.author
    voice_state = author.voice
    if voice_state is None:
        return

    # Step 2. 연결되어 있는 보이스채널 돌아가면서 보낸 메세지와 일치하는 서버가 있다면 그 서버에서 재생 중단
    voice_clients = client.voice_clients
    if len(voice_clients) == 0:
        return

    for voice_client in voice_clients:
        if message.guild == voice_client.guild:
            if voice_client.is_playing():
                await voice_client.stop()
            await voice_client.disconnect()
