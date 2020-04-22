__author__ = 'gecheng'

from output.tableToDictionary import tableToDic
from blackJack import blackJackGame
import random as rn



strategyTables = ['output/hard_table.csv', 'output/soft_table.csv', 'output/pair_table.csv']
#strategyTables = ['strategy_compare/Hard_Table_Strategy.csv', 'strategy_compare/Soft_Table_Strategy.csv', 'strategy_compare/Pair_Table_Strategy.csv']


hard_table = tableToDic(strategyTables[0])
soft_table = tableToDic(strategyTables[1])
pair_table = tableToDic(strategyTables[2])


table_dic = {}
table_dic['hard'] = hard_table
table_dic['soft'] = soft_table
table_dic['pair'] = pair_table


def playerOperation(bl, ip, table_dic):
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

    point = point + min([int((21-point)/10), An]) * 10
    if min([int((21-point)/10), An]) == 0:
        type = 'hard'
    else:
        type = 'soft'


    dealerPoint = 0
    card = bl.dealer[0]
    if card[0] in ['T' , 'J', 'Q', 'K']:
       dealerPoint += 10
    elif card[0] == 'A':
       dealerPoint += 11
    else:
       dealerPoint += int(card[0])


    if len(bl.players[ip]) == 2 and bl.players[ip][0][0] == bl.players[ip][1][0] and bl.split[ip] == 0:

        if bl.players[ip][0][0] == 'A':
            tempPoint = 22
        else:
            tempPoint = point

        opt = table_dic['pair'][str(tempPoint) + ',' + str(dealerPoint)]
        if opt == 'SP':
            return 'split'
        elif opt == 'H':
            return 'hit'
        elif opt == 'S':
            return 'std'
        elif opt == 'D':
            return 'double'
    elif point < 5:
        return 'hit'
    else:
        opt = table_dic[type][str(point) + ',' + str(dealerPoint)]

        if opt == 'H':
            return 'hit'
        elif opt == 'S':
            return 'std'
        elif opt == 'D' and len(bl.players[ip]) == 2:
            return 'double'
        elif opt == 'D' and len(bl.players[ip]) != 2:
            return 'hit'


rn.seed(1)

finalScores = []

for i in range(100000):
    bl = blackJackGame(1)
    while bl.finish == 0:
        for ip, player in enumerate(bl.players):
            if bl.bust[ip] == 0 and bl.standings[ip] == 0:
                ope = playerOperation(bl, ip, table_dic)
                print(bl.players, bl.dealer)
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









