import configparser
import os


config = configparser.ConfigParser()
config.read('./config.ini')

GAME_STATUS = '"!도움"'

###################### 환경 상수 ################################
DISCORD_TOKEN = config['DEFAULT']['DISCORD_TOKEN']
DATA_DIR = os.path.abspath(config['DEFAULT']['DATA_DIR'])
############################################################

#########   명령어 상수 정의     ##########################################################################
COMMAND_REACTION1 = '!리액션'
COMMAND_REACTION2 = '!react'
COMMAND_HELP1 = '!도움'
COMMAND_HELP2 = '!help'
# COMMAND_LOLSTAT = '!롤전적'
# COMMAND_LOLNOW = '!롤현재'
# COMMAND_URF = '!우르프'
COMMAND_R6STAT = '!레식전적'
COMMAND_R6OPER = '!레식오퍼'
COMMAND_APEX = '!에이펙스'
COMMAND_CLEAR1 = '!정리'
COMMAND_CLEAR2 = '!clear'
COMMAND_VOTE = '!투표'
COMMAND_TEAM = '!팀나누기'
COMMAND_JEBI = '!제비뽑기'
COMMAND_BOTCTL = '!봇조종'
COMMAND_BOTSAY = '!봇말'
COMMAND_REACTION_UPLOAD = '!리액션업로드'
COMMAND_STOP_PLAYING = '!중단'
COMMAND_TEAM_VOICED = '!음성팀나누기'
COMMAND_REPLAY_PUBG = '!리플레이배그' # BETA
COMMAND_REPLAY_LOL = '!리플레이롤'    # BETA


COMMAND_LIST = [
    COMMAND_REACTION1,
    COMMAND_REACTION2,
    COMMAND_HELP1,
    COMMAND_HELP2,
    # COMMAND_LOLSTAT,
    # COMMAND_LOLNOW,
    # COMMAND_URF,
    COMMAND_R6STAT,
    COMMAND_R6OPER,
    COMMAND_APEX,
    COMMAND_CLEAR1,
    COMMAND_CLEAR2,
    COMMAND_VOTE,
    COMMAND_TEAM,
    COMMAND_JEBI,
    COMMAND_BOTCTL,
    COMMAND_BOTSAY,
    COMMAND_REACTION_UPLOAD,
    COMMAND_STOP_PLAYING,
    COMMAND_TEAM_VOICED,
    COMMAND_REPLAY_PUBG,
    COMMAND_REPLAY_LOL,
]

HELP_LIST = [
    [COMMAND_HELP1 + ', ' + COMMAND_HELP2, '명령어 리스트를 보여줍니다.', COMMAND_HELP1 + '` or `' + COMMAND_HELP2],
    # [COMMAND_LOLSTAT, '롤 전적을 보여줍니다.', COMMAND_LOLSTAT],
    # [COMMAND_LOLNOW, '현재 플레이중인 롤 정보를 보여줍니다.', COMMAND_LOLNOW],
    # [COMMAND_URF, '현재 우르프 티어를 보여줍니다.', COMMAND_URF],
    [COMMAND_R6STAT, '레인보우식스 시즈 전적을 보여줍니다.', COMMAND_R6STAT + ' (아이디)'],
    [COMMAND_R6OPER, '레인보우식스 시즈 오퍼레이터 순위를 플레이타임 순으로 보여줍니다.', COMMAND_R6OPER + ' (아이디)'],
    [COMMAND_APEX, '에이펙스 레전드 전적을 보여줍니다.', COMMAND_APEX + ' (아이디)'],
    [COMMAND_REACTION1, '보이스챗 리액션을 할 수 있습니다. 자세한 정보는 `!리액션`에서.', COMMAND_REACTION1 + ' (리스트) or ' + \
                                                                                    COMMAND_REACTION2 + ' (리스트)'],
    [COMMAND_TEAM, '팀을 나눌 수 있습니다.', COMMAND_TEAM + ' (팀 수)'],
    [COMMAND_TEAM_VOICED, '현재 접속해 있는 음성채널 멤버를 기준으로 팀을 나눕니다', COMMAND_TEAM_VOICED + ' (팀 수)'],
    [COMMAND_JEBI, '제비뽑기를 할 수 있습니다.', COMMAND_JEBI + ' (뽑을 사람 수)'],
    [COMMAND_STOP_PLAYING, '현재 재생 중인 음악 혹은 리액션을 중단하고 나갑니다.', COMMAND_STOP_PLAYING],
    [COMMAND_REPLAY_PUBG, '배그 리플레이를 웹페이지에서 볼 수 있습니다. (베타)', COMMAND_REPLAY_PUBG + ' (아이디)'],
    [COMMAND_REPLAY_LOL, '롤 리플레이를 웹페이지에서 볼 수 있습니다. (베타)', COMMAND_REPLAY_LOL + ' (아이디)'],
]

ADMIN_HELP_LIST = [
    [COMMAND_REACTION_UPLOAD, '서버에 리액션을 업로드 할 수 있습니다.', COMMAND_R6STAT],
    # [COMMAND_R6OPER, '레인보우식스 시즈 오퍼레이터 순위를 플레이타임 순으로 보여줍니다.', COMMAND_R6OPER + ' (아이디)'],
    # [COMMAND_APEX, '에이펙스 레전드 전적을 보여줍니다.', COMMAND_APEX + ' (아이디)'],
    # [COMMAND_REACTION1, '보이스챗 리액션을 할 수 있습니다. 자세한 정보는 `!리액션`에서.', COMMAND_REACTION1 + ' (리스트) or ' + \
    #                                                                                 COMMAND_REACTION2 + ' (리스트)'],
    # [COMMAND_TEAM, '팀을 나눌 수 있습니다.', COMMAND_TEAM + ' <팀 수>'],
    # [COMMAND_JEBI, '제비뽑기를 할 수 있습니다.', COMMAND_JEBI + ' (뽑을 사람 수)'],
    # [COMMAND_STOP_PLAYING, '현재 재생중인 음악 혹은 리액션을 중단하고 나갑니다.', COMMAND_STOP_PLAYING]
]


# .format(id) 와 같이 사용
DATA_DIR_ID_FORMAT = DATA_DIR + '/{}/'
MUSIC_DIR_ID_FORMAT = DATA_DIR + '/{}/music/'

REACTION_DEFAULT_DIR = MUSIC_DIR_ID_FORMAT.format('default')

##########################################################################################################