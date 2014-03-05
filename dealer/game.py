import itertools
import random
from collections import deque

from pokereval.card import Card
from pokereval.hand_evaluator import HandEvaluator

from dealer.cards import Cards
from dealer.players import Player
from dealer import config

phases = ('pre-flop', 'flop', 'turn', 'river')
cards_for_phase = {'pre-flop':0, 'flop':3, 'turn':4, 'river':5}


class Game:

    def __init__(self):
        self.distribution = 1
        self.players = deque([Player(player_id, player_data)
                for player_id, player_data in config.PLAYERS.items()])

    def shuffle(self):
        random.shuffle(self.cards.deck)

    def deal(self):
        for player in self.players:
            player.hand.append(self.cards.deck.pop())
            player.hand.append(self.cards.deck.pop())

    def next_deal(self):
        if getattr(self, 'pot', None):
            winner = self.winner()
            winner.account += self.pot
        self.cards = Cards()
        self.phases = iter(phases)
        self.phase = next(self.phases)
        self.pot = 0
        self.distribution += 1
        self.rotate_players()
        self.players_iter = iter(self.players)
        self.shuffle()
        self.deal()
        self.bet = None

    def rotate_players(self):
        for player in self.players:
            player.new_distribution()
        self.players.rotate()

    def next_phase(self):
        try:
            self.phase = next(self.phases)
        except StopIteration:
            self.next_deal()
        self.players_iter = iter(self.players)

    def play(self):
        if len([i for i in self.players if i.active]) > 1:
            for player in self.players_iter:
                if player.active:
                    data = {
                        'table': [],
                        'min': 0,
                        'bids': {},
                    }
                    self.actual_player = player.name
                    bet = player.bet(data)
                    bet = self.validate_bet(player, bet, data)
                    self.pot += bet
                    self.bet = bet
                    return
            self.next_phase()
            self.actual_player = None
        else:
            self.next_deal()

    def validate_bet(self, player, bet, data):
        if bet:
            player.account -= bet
        else:
            player.active = False
        return bet

    def winner(self):
        winner = None
        table = self.cards.deck[:5]
        for player in  self.players:
            if not player.active:
                continue
            print(player.name, player.hand_value(table))
            if not winner:
                winner = player
                continue
            if player.hand_value(table) > winner.hand_value(table):
                winner = player
        return winner

game = Game()
game.next_deal()
