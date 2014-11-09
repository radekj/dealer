START_ACCOUNT = 500
SMALL_BLIND = 5
BIG_BLIND = 10
MAX_BET_LIMIT = 20
DISTRIBUTION = 0
SHOW_HAND_CARDS = True

PLAYERS = {
    'player1': {
        'name': 'Player 1',
        'account': START_ACCOUNT,
        'address': 'localhost:4000',
    },
    'player2': {
        'name': 'Player 2',
        'account': START_ACCOUNT,
        'address': 'localhost:4001',
    },
    'player3': {
        'name': 'Player 3',
        'account': START_ACCOUNT,
        'address': 'localhost:4002',
    },
    'player4': {
        'name': 'Player 4',
        'account': START_ACCOUNT,
        'address': 'localhost:4003',
    },
    # 'player5': {
    #     'name': 'Player 5',
    #     'account': START_ACCOUNT,
    #     'address': 'localhost:4000',
    # },
    # 'player6': {
    #     'name': 'Player 6',
    #     'account': START_ACCOUNT,
    #     'address': 'localhost:4000',
    # },
    # 'player7': {
    #     'name': 'Player 7',
    #     'account': START_ACCOUNT,
    #     'address': 'localhost:4000',
    # },
    # 'player8': {
    #     'name': 'Player 8',
    #     'account': START_ACCOUNT,
    #     'address': 'localhost:4000',
    # },
}

# uncomment to use save
#from .saves.save_YYYYMMDDHHMMSS import *
