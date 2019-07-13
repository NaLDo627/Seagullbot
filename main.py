import discord
from constant import *
from commands import cmdparser
import os

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')
    await client.change_presence(activity=discord.Game(name=GAME_STATUS))


@client.event
async def on_server_join(server):
    # [190308][HKPARK] 서버 입장시 data/music/(서버ID) 식으로 폴더 생성한다.
    # [190313][HKPARK] 폴더 경로를 data/(서버ID)/music 식으로 변경.
    # [190714][HKPARK] 이제 폴더 경로를 환경 상수에서 가져옴.
    try:
        music_path = MUSIC_DIR_ID_FORMAT.format(server.id)
        if not (os.path.isdir(music_path)):
            os.makedirs(os.path.join(music_path))
            filepath = os.path.join(music_path, server.name + ".txt")
            fid = open(filepath, "w")
            if not os.path.isfile(filepath):
                fid.write(server.name)

            fid.close()
    except OSError as e:
        print('ERROR: ' + str(e))
        return


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    argv = message.content.split()
    argc = len(argv)

    if argv[0] not in COMMAND_LIST:
        return

    await cmdparser.parse_command(argc, argv, client, message)


client.run(DISCORD_TOKEN)
