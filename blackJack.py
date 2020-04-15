__author__ = 'gecheng'

import random as rn

class blackJackGame():
    def __init__(self):
        self.cards = []
        rank = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
        suit = ['s', 'h', 'c', 'd']
        for i in range(2):
            for r in rank:
                for s in suit:
                    self.cards.append(r+s)

        self.players = []
        index = rn.sample(range(len(self.cards)),1)
        self.players.append([self.cards.pop(index[0])])
        index = rn.sample(range(len(self.cards)),1)
        self.players[0].append(self.cards.pop(index[0]))


        self.points = []
        self.points.append(0)



        index = rn.sample(range(len(self.cards)),1)
        self.dealer = [self.cards.pop(index[0])]
        index = rn.sample(range(len(self.cards)),1)
        self.dealer.append(self.cards.pop(index[0]))




        self.dealerBust = 0
        self.dealerPoint = 0

        self.bets = []
        self.bets.append(1)

        self.standings = []
        self.standings.append(0)

        self.bust = []
        self.bust.append(0)

        self.split = 0

        self.finish = 0

        self.finalScore = 0


    def playerOperation(self, ip, ope):

        if ope == 'double':
            self.bets[ip] = self.bets[ip] * 2
            self.playerOperation(self,ip, 'hit')
            self.standings[ip] = 1
            self.checkBustout()
        if ope == 'split':
            if len(self.players[ip]) != 2 or self.players[ip][0][0] != self.players[ip][1][0] or self.split == 1:
                raise Exception(print('Split Error'))

            self.players[ip] = [self.players[ip][0]]
            self.players.append([self.players[ip][1]])


            self.bets.append(self.bets[ip])
            self.standings.append(0)
            self.bust.append(0)
            self.points.append(0)

            if self.players[ip][0][0] == 'A':
                self.playerOperation(self, ip, 'hit')
                self.playerOperation(self, len(self.players)-1, 'hit')
                self.standings[ip] = 1
                self.standings[len(self.players) -1] = 1

            self.split = 1
            self.checkBustout()

        if ope == 'hit':
            index = rn.sample(range(len(self.cards)),1)
            self.players[ip].append(self.cards.pop(index[0]))
            self.checkBustout()

        if ope == 'std':
            self.standings[ip] = 1

    def checkStatus(self):
        if sum(self.standings) + sum(self.bust) == len(self.players):
            self.finish = 1

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


    def finalScoreCal(self):
        ### To Do: Consider Blackjack
        if self.dealerBust == 1:
            for ip, player in enumerate(self.players):
                if self.bust[ip] == 0:
                    self.finalScore = self.finalScore + self.bets[ip]
        elif self.dealerBust == 0:
            for ip, player in enumerate(self.players):
                if self.bust[ip] == 1:
                    self.finalScore = self.finalScore - self.bets[ip]
                elif self.bust[ip] == 0:
                    if self.dealerPoint > self.points[ip]:
                        self.finalScore = self.finalScore - self.bets[ip]
                    elif self.dealerPoint < self.points[ip]:
                        self.finalScore = self.finalScore + self.bets[ip]


def strategy(bl, ip):
    point = 0
    An = 0
    for card in bl.players[ip]:
        if card[0] in ['T' , 'J', 'Q', 'K']:
            point += 10
        elif card[0] == 'A':
            point += 1
            An += 1
        else:
            point += int(card[0])

    if point + min([int((21-point)/10), An]) * 10 >= 17:
        return 'std'
    else:
        return 'hit'




rn.seed(1)

finalScores = []

for i in range(10000):
    bl = blackJackGame()
    while bl.finish == 0:
        for ip, player in enumerate(bl.players):
            if bl.bust[ip] == 0:
                ope = strategy(bl, ip)
                bl.playerOperation(ip, ope)

        bl.checkStatus()
        if bl.finish == 1:
            bl.dealerDraw()
            bl.dealerPointCal()
            bl.playerPoint()
            bl.finalScoreCal()


    print("player hand")
    print(bl.players)
    print("dealer hand")
    print(bl.dealer)
    print("player bust")
    print(bl.bust)
    print("dealer bust")
    print(bl.dealerBust)
    print("player point")
    print(bl.points)
    print("dealer point")
    print(bl.dealerPoint)
    print("score")
    print(bl.finalScore)
    print("Number of cards")
    print(len(bl.cards))

    finalScores.append(bl.finalScore)


print("total Score")
print(sum(finalScores))