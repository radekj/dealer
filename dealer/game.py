import itertools
import random
from collections import deque

from pokereval.card import Card
from pokereval.hand_evaluator import HandEvaluator

from dealer.cards import Cards
from dealer.players import Player
from dealer import config

phases = ('pre-flop', 'flop', 'turn', 'river')
cards_for_phase = {'pre-flop': 0, 'flop': 3, 'turn': 4, 'river': 5}


class Game:

    def __init__(self):
        self.distribution = 1
        self.players = deque([
            Player(player_id, player_data)
            for player_id, player_data in config.PLAYERS.items()
        ])

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
            if not self.shown:
                self.bet = 1
                self.shown = True
                return
        self.cards = Cards()
        self.phases = iter(phases)
        self.phase = next(self.phases)
        self.pot = 0
        self.distribution += 1
        self.rotate_players()
        self.players_iter = itertools.cycle(self.players)
        self.shuffle()
        self.deal()
        self.bet = 0
        self.shown = False
        self.num = 0

    def rotate_players(self):
        for player in self.players:
            player.new_distribution()
        self.players.rotate()
        self.players = deque([i for i in self.players if i.active])

    def next_phase(self):
        try:
            self.phase = next(self.phases)
        except StopIteration:
            return self.next_deal()

        for player in self.players:
            player.deal_bet = 0
        self.bet = 0
        self.num = 0
        self.players_iter = itertools.cycle(self.players)

    def play(self):
        active_players = len([i for i in self.players if i.active]) > 1
        all_equal = len(set([i.deal_bet for i in self.players if i.active])) == 1

        if active_players:
            if not all_equal or not self.bet:
                for player in self.players_iter:
                    if self.num == len(self.players) and not self.bet:
                        break
                    blind = 0
                    if self.phase == 'pre-flop' and self.num == 0:
                        blind = config.SMALL_BLIND
                    elif self.phase == 'pre-flop' and self.num == 1:
                        blind = config.BIG_BLIND
                    self.num += 1
                    if player.active:
                        data = {
                            'hand': player.hand,
                            'table': self.cards.deck[:cards_for_phase[self.phase]],
                            'min': self.bet - player.deal_bet,
                            'can_raise': not player.deal_bet > 0,
                            'pot': self.pot,
                            'account': player.account,
                            'limit': config.MAX_BET_LIMIT,
                        }
                        self.actual_player = player.name
                        if not blind:
                            bet = player.bet(data)
                            bet = self.process_bet(player, bet, data)
                        else:
                            bet = blind
                            self.process_bet(player, bet, data)
                        if bet:
                            player.deal_bet += bet
                            self.bet = player.deal_bet
                        self.pot += bet
                        return
            self.next_phase()
            self.actual_player = None
        else:
            self.actual_player = None
            self.next_deal()

    def process_bet(self, player, bet, data):
        bet = self.validate_bet(player, bet, data)
        if bet:
            if player.deal_bet + bet >= self.bet:
                player.account -= bet
                return bet
        if data.get('min'):
            player.active = False
        return 0

    def validate_bet(self, player, bet, data):
        try:
            assert isinstance(bet, int)
            assert (bet <= data['limit'] + data['min'])
            assert (bet >= data['min'] or bet == 0)
            assert (bet <= data['account'])
            if not data['can_raise']:
                assert (bet == 0 or bet == data['min'])
            return bet
        except AssertionError:
            return 0

    def winner(self):
        winner = None
        table = self.cards.deck[:5]
        for player in self.players:
            if not player.active:
                continue
            if not winner:
                winner = player
                continue
            if player.hand_value(table) > winner.hand_value(table):
                winner = player
        winner.winner = True
        return winner

game = Game()
game.next_deal()
