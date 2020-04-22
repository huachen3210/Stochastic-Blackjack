__author__ = 'gecheng'

import random as rn

import random as rn

class blackJackGame():
    # initial the game
    def __init__(self, player_num):

        # initial two deck of cards
        self.cards = []
        rank = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
        suit = ['s', 'h', 'c', 'd']
        for i in range(2):
            for r in rank:
                for s in suit:
                    self.cards.append(r+s)


        self.players = []
        self.points = []
        self.bets = []
        self.standings = []
        self.bust = []
        self.split = []


        for id in range(player_num):
            # initial players as list, each player draw two cards
            index = rn.sample(range(len(self.cards)),1)
            self.players.append([self.cards.pop(index[0])])
            index = rn.sample(range(len(self.cards)),1)
            self.players[id].append(self.cards.pop(index[0]))

            # initial points of player, set as 0
            self.points.append(0)

            # bet for each player
            self.bets.append(1)

            # whether player standing
            self.standings.append(0)

            # whether player bust
            self.bust.append(0)

            # whether player split
            self.split.append(0)



        # initial dealer hands, draw two cards
        index = rn.sample(range(len(self.cards)),1)
        self.dealer = [self.cards.pop(index[0])]
        index = rn.sample(range(len(self.cards)),1)
        self.dealer.append(self.cards.pop(index[0]))



        # whether dealer bust
        self.dealerBust = 0
        # point of dealer hand
        self.dealerPoint = 0


        # whether players finish all operation
        self.finish = 0

        # the final score for the player
        self.finalScore = 0

    # get the operation for ip th player
    def playerOperation(self, ip, ope):


        # double operation
        if ope == 'double':
            if len(self.players[ip]) != 2:
                raise Exception(print('double Error'))

            self.bets[ip] = self.bets[ip] * 2
            self.playerOperation(ip, 'hit')
            self.checkBustout()
            if self.bust[ip] != 1:
                self.standings[ip] = 0


        # split operation
        if ope == 'split':
            if len(self.players[ip]) != 2 or self.players[ip][0][0] != self.players[ip][1][0] or self.split[ip] == 1:
                raise Exception(print('Split Error'))


            self.players.append([self.players[ip][1]])
            self.players[ip] = [self.players[ip][0]]


            self.bets.append(self.bets[ip])
            self.standings.append(0)
            self.bust.append(0)
            self.points.append(0)
            self.split.append(1)

            if self.players[ip][0][0] == 'A':
                self.playerOperation(ip, 'hit')
                self.playerOperation(len(self.players)-1, 'hit')
                self.standings[ip] = 1
                self.standings[len(self.players) -1] = 1

            self.split[ip] = 1

            self.checkBustout()


        # hit operation
        if ope == 'hit':
            if self.standings[ip] == 0:
                index = rn.sample(range(len(self.cards)),1)
                self.players[ip].append(self.cards.pop(index[0]))
                self.checkBustout()
            else:
                raise Exception(print('Hit Error'))

        # standing operation
        if ope == 'std':
            self.standings[ip] = 1

    # check whether the game will continue(whether all player have "standing" or "bust")
    def checkStatus(self):
        if sum(self.standings) + sum(self.bust) == len(self.players):
            self.finish = 1


    # check whether player bust
    def checkBustout(self):
        for ip, player in enumerate(self.players):
            point = 0
            for card in player:
                if card[0] in ['T' , 'J', 'Q', 'K']:
                    point += 10
                elif card[0] == 'A':
                    point += 1
                else:
                    point += int(card[0])
            if point > 21:
                self.bust[ip] = 1

    # dealer draw card
    def dealerDraw(self):
        if sum(self.standings) > 0:

            softThreshold = 0
            point = 0
            An = 0

            for card in self.dealer:
               if card[0] in ['T' , 'J', 'Q', 'K']:
                   point += 10
               elif card[0] == 'A':
                   point += 1
                   An = An + 1
               else:
                   point += int(card[0])

            softPoint = point + min([int((21-point)/10) , An])*10


            if softPoint >= 17 and point <= 21:
                softThreshold = 1


            while softThreshold == 0 and self.dealerBust == 0:

                index = rn.sample(range(len(self.cards)),1)
                self.dealer.append(self.cards.pop(index[0]))

                card = self.dealer[len(self.dealer)-1]
                if card[0] in ['T' , 'J', 'Q', 'K']:
                    point += 10
                elif card[0] == 'A':
                    point += 1
                    An += 1
                else:
                    point += int(card[0])

                softPoint = point + min([int((21-point)/10) , An])*10
                if softPoint >= 17 and point <= 21:
                    softThreshold = 1
                if point > 21:
                    self.dealerBust = 1

    # calculate points of player hand
    def playerPoint(self):
        if sum(self.standings) > 0:
            for ip, player in enumerate(self.players):
                if self.bust[ip] == 0:
                     point = 0
                     An = 0
                     for card in self.players[ip]:
                         if card[0] in ['T' , 'J', 'Q', 'K']:
                              point += 10
                         elif card[0] == 'A':
                             point += 1
                             An += 1
                         else:
                             point += int(card[0])
                     self.points[ip] = point + min([int((21-point)/10), An]) * 10

    # calculate points of dealer hand
    def dealerPointCal(self):
        if self.dealerBust == 0 and sum(self.standings) > 0:
            point = 0
            An = 0
            for card in self.dealer:
                 if card[0] in ['T' , 'J', 'Q', 'K']:
                     point += 10
                 elif card[0] == 'A':
                     point += 1
                     An += 1
                 else:
                     point += int(card[0])
            self.dealerPoint = point + min([int((21-point)/10), An]) * 10



    # calculate final score of players
    def finalScoreCal(self):
        for ip, player in enumerate(self.players):
            if self.bust[ip] == 1:
                self.finalScore =self.finalScore + (-1) * self.bets[ip]

            if self.bust[ip] == 0:
                if self.dealerBust == 0:
                    if self.dealerPoint > self.points[ip]:
                        self.finalScore = self.finalScore - self.bets[ip]
                    elif self.dealerPoint < self.points[ip]:
                        if len(self.players[ip]) == 2 and self.points[ip] == 21:
                            self.finalScore = self.finalScore + self.bets[ip]*1.5
                        else:
                            self.finalScore = self.finalScore + self.bets[ip]

                    elif self.dealerPoint == self.points[ip] and self.dealerPoint == 21:
                        if len(self.players[ip]) == 2:
                            if len(self.dealer) != 2:
                                self.finalScore = self.finalScore + 1.5 * self.bets[ip]
                        elif len(self.players[ip]) != 2:
                            if len(self.dealer) == 2:
                                self.finalScore = self.finalScore - self.bets[ip]

                elif self.dealerBust == 1:
                    if len(self.players[ip]) == 2 and self.points[ip] == 21:
                        self.finalScore = self.finalScore + self.bets[ip]*1.5
                    else:
                        self.finalScore = self.finalScore + self.bets[ip]


