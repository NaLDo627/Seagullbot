import discord
from commands.gamestats import apexlegends as apex
from commands.gamestats import siege
from constant import *
from commands.botutils import common
from commands.botutils import voiceutils
from commands.botutils import admin


async def parse_command(argc, argv, client, message):
    #########   봇 공용 명령어     ##########################################################################
    # !끼룩
    if argv[0] == "!끼룩":
        await message.channel.send("끼룩!")

    # !도움
    if argv[0] == COMMAND_HELP1 or argv[0] == COMMAND_HELP2:
        await common.show_help(client, message)

    # !정리
    elif argv[0] == COMMAND_CLEAR1 or argv[0] == COMMAND_CLEAR2:
        await common.clear_command(client, message)

    # !투표
    elif argv[0] == COMMAND_VOTE:
        await common.vote_by_reaction(argc, argv, client, message)

    # !팀나누기
    elif argv[0] == COMMAND_TEAM:
        await common.divide_team_by_text(argc, argv, client, message)

    # !음성팀나누기
    elif argv[0] == COMMAND_TEAM_VOICED:
        await common.divide_team_by_voice_channel(argc, argv, client, message)

    # !제비뽑기
    elif argv[0] == COMMAND_JEBI:
        await common.lottery(argc, argv, client, message)

    ################################ 음성 명령어 ###########################################################
    # !리액션
    elif argv[0] == COMMAND_REACTION1 or argv[0] == COMMAND_REACTION2:
        await voiceutils.play_reaction(argc, argv, client, message)

    # !중단
    elif argv[0] == COMMAND_STOP_PLAYING:
        await voiceutils.stop_playing(argc, argv, client, message)
    ##########################################################################################################

    ##########################################################################################################
    #
    # #########   롤 관련 명령어     ##########################################################################
    #     # !롤전적
    #     elif argv[0] == COMMAND_LOLSTAT:
    #         await client.send('아이디를 입력하세요.')
    #         msg = await client.wait_for_message(timeout=15.0, author=message.author)
    #
    #         if msg is None:
    #             await client.send('입력받은 아이디가 없습니다.')
    #             return
    #         elif msg.content == '항상최선을다해서':
    #             embed = discord.Embed(title='함부로 그를 검색하지 마십시오. 경고합니다.',
    #                                   description='warning.or.kr',
    #                                   color=0x00ff00)
    #             await client.send(embed=embed)
    #         else:
    #             embed = discord.Embed(title='최근 전적',
    #                                   description='[OP.GG](http://www.op.gg/summoner/userName=' + msg.content.replace(" ", "") + ')',
    #                                   color=0x00ff00)
    #             embed.set_thumbnail(url="http://opgg-static.akamaized.net/images/profile_icons/profileIcon27.jpg")
    #             await client.send(embed=embed)
    #
    #     # !롤현재
    #     elif argv[0] == COMMAND_LOLNOW:
    #         if len(message.content.split(' ')) == 1:
    #             searching = await client.send('아이디를 입력하세요.')
    #             msg = await client.wait_for_message(timeout=15.0, author=message.author)
    #             player_id = msg.content
    #             await client.delete_message(msg)
    #
    #             if msg is None:
    #                 await client.send('입력받은 아이디가 없습니다.')
    #                 await client.delete_message(searching)
    #                 return
    #             else:
    #                 searching = await client.edit_message(searching, '검색중입니다...')
    #                 await client.send_typing(message.channel)
    #         else:
    #             player_id = message.content.split(' ')[1]
    #             searching = await client.send('검색중입니다...')
    #             await client.send_typing(message.channel)
    #
    #         temp = lol.search(player_id)
    #         if temp == 1:
    #             embed = discord.Embed(title='NOW PLAYING: **'+ lol.find_champion_name(player_id).upper() + '**',
    #                                   description='[OP.GG](http://www.op.gg/summoner/userName='+ player_id.replace(" ", "") + ') 에서 확인해보세요.',
    #                                   color=0x00ff00)
    #             embed.set_thumbnail(url=lol.find_champion_img(player_id))
    #             await client.delete_message(searching)
    #             await client.send(embed=embed)
    #         elif temp == 0:
    #             embed = discord.Embed(title=player_id + ' is not playing right now. :zzz:',
    #                                   description='다른 사람을 검색하시려면 `!롤현재 (아이디)`',
    #                                   color=0xed2902)
    #             await client.delete_message(searching)
    #             await client.send(embed=embed)
    #
    # ##########################################################################################################
    #
    # #########   우르프 관련 명령어     ######################################################################
    #     # !우르프
    #     elif argv[0] == COMMAND_URF:
    #         await client.send('***:zap: URF TIER LIST :zap:** presented by* op.gg')
    #         (champions, winrate, kda) = urf.urf_rank()
    #         s = "```CHAMPION                                 WINRATE      KDA\n\n"
    #         index = 1
    #
    #         while index < 11:
    #             if index == 10:
    #                 s += str(index)+ '.' + str(champions[index-1]).ljust(38) + str(winrate[index-1]) + '       ' + str(kda[index-1]) + '\n'
    #             else:
    #                 s += str(index) + '. ' + str(champions[index - 1]).ljust(38)+ str(winrate[index - 1]) + '       ' + str(kda[index - 1]) + '\n'
    #
    #             index += 1
    #         s += "```"
    #
    #         await client.send(s)
    #
    # ##########################################################################################################

    #########   레식 관련 명령어     ########################################################################
    # !레식전적
    elif argv[0] == COMMAND_R6STAT:
        await siege.siege_search_stats(argc, argv, client, message)

    # !레식오퍼
    elif argv[0] == COMMAND_R6OPER:
        await siege.siege_search_operator(argc, argv, client, message)

    ##########################################################################################################

    ###################에이펙스 관련 명령어 ##################################################################
    # !에이펙스
    elif argv[0] == COMMAND_APEX:
        searching = None

        def is_caller(m):
            return m.author == message.author

        if argc == 1:
            searching = await message.channel.send('아이디를 입력하세요.')
            msg = await client.wait_for('message', timeout=15.0)
            player_id = msg.content

            await msg.delete()
            # await message.channel.delete_message(msg)

            if msg is None:
                await message.channel.send('입력받은 아이디가 없습니다.', delete_after=10)
                await searching.delete()
                return
            # searching = await message.channel.edit_message(searching, '검색중입니다...')
            await searching.edit(content='검색중입니다...')
            # await message.channel.send_typing(message.channel)
        else:
            player_id = message.content.split(' ')[1]
            searching = await message.channel.send('검색중입니다...')
            await message.channel.send_typing(message.channel)

        # async with message.channel.typing():
        await message.channel.trigger_typing()
        result = apex.search(player_id)
        if result == -1:
            await searching.edit(content='플레이어를 찾을 수 없습니다.', delete_after=10)
        else:
            embed = discord.Embed(title='플레이어: **' + player_id + '**',
                                  description='```' + result + '```\n 더 많은 정보는 [여기서](https://apex.tracker.gg/profile/pc/'
                                              + player_id + ')',
                                  color=0x00ff00)
            await message.channel.delete_message(searching)
            await message.channel.send(embed=embed)

    ##########################################################################################################

    ################################ 리플레이 UI 연동 명령어 #################################################

    # !리플레이배그
    elif argv[0] == COMMAND_REPLAY_PUBG:
        await common.replay_ui_pubg(argc, argv, client, message)

    # !리플레이롤
    elif argv[0] == COMMAND_REPLAY_LOL:
        await common.replay_ui_lol(argc, argv, client, message)

    ##########################################################################################################

    ################################ 관리자 명령어 ###########################################################
    #
    # # 권한체크
    # if not admin.check_admin_role(message.author, message.channel):
    #     await message.channel.send("이 명령어를 사용할 권한이 없습니다.", delete_after=10)
    #     return

    # !봇조종
    if argv[0] == COMMAND_BOTCTL:
        await admin.set_target_channel_to_say(argc, argv, client, message)

    # !봇말
    elif argv[0] == COMMAND_BOTSAY:
        await admin.say_bot_to_channel(argc, argv, client, message)

    # !리액션업로드
    elif argv[0] == COMMAND_REACTION_UPLOAD:
        await admin.upload_reaction(argc, argv, client, message)

    elif argv[0] == '!끼룩':
        await message.channel.send('https://www.youtube.com/watch?v=m6qWcKLB7Ig')

