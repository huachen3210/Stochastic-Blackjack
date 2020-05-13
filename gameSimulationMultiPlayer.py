__author__ = 'gecheng'

from utils import tableToDic
from blackJack import blackJackGame
import random as rn
import numpy as np


ratios = [i/100 for i in range(20,35)]

strategyTablesDic = dict()

for i in range(len(ratios)):
    #print('multiPlayer/output_' + str(ratios[i])+'/hard_table_' + str(ratios[i]) + '.csv')
    strategyTables = ['multiPlayer/output_' + str(ratios[i])+'/hard_table_' + str(ratios[i]) + '.csv', 'multiPlayer/output_' + str(ratios[i])+'/soft_table_' + str(ratios[i]) + '.csv', 'multiPlayer/output_' + str(ratios[i])+'/pair_table_' + str(ratios[i]) + '.csv']
    hard_table = tableToDic(strategyTables[0])
    soft_table = tableToDic(strategyTables[1])
    pair_table = tableToDic(strategyTables[2])

    strategyTablesDic[ratios[i]] = {}
    strategyTablesDic[ratios[i]]['hard'] = hard_table
    strategyTablesDic[ratios[i]]['soft'] = soft_table
    strategyTablesDic[ratios[i]]['pair'] = pair_table



'''
#strategyTables = ['output/hard_table.csv', 'output/soft_table.csv', 'output/pair_table.csv']
strategyTables = ['Basic_strategy_baseline/Hard_Table_Strategy.csv', 'Basic_strategy_baseline/Soft_Table_Strategy.csv', 'Basic_strategy_baseline/Pair_Table_Strategy.csv']


hard_table = tableToDic(strategyTables[0])
soft_table = tableToDic(strategyTables[1])
pair_table = tableToDic(strategyTables[2])


table_dic = {}
table_dic['hard'] = hard_table
table_dic['soft'] = soft_table
table_dic['pair'] = pair_table

'''



def playerOperation(bl, ip, strategyTablesDic, insurance  = False):

    if ip <= 3:
        return 'hit'

    cardStrings = ''.join(bl.cards)
    tenRatio = (cardStrings.count('T') + cardStrings.count('J') + cardStrings.count('Q') + cardStrings.count('K'))/len(bl.cards)

    if insurance == True:
        if bl.dealer[0][0] == 'A':
            if tenRatio >= 1/3:
                return 'ins'
            else:
                return  'notIns'

    tenRatio = round(tenRatio, 2)

    if tenRatio < 0.2:
        tenRatio = 0.2
    elif tenRatio > 0.34:
        tenRatio = 0.34

    table_dic = strategyTablesDic[tenRatio]

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





rn.seed(123)
finalScores = []
finalBets = []


for i in range(100000):

    bl = blackJackGame(5, [0.001, 0.001, 0.001, 0.001, 4.996])

    for ip, player in enumerate(bl.players):

        ins_ope = playerOperation(bl, ip, strategyTablesDic, True)
        if ins_ope == 'ins':
            bl.playerOperation(ip, 'ins')

        while bl.standings[ip] == 0 and bl.bust[ip] == 0:
            ope = playerOperation(bl, ip, strategyTablesDic)
            bl.playerOperation(ip, ope)
            #if bl.bust[ip] == 0 and bl.standings[ip] == 0:
            #    ope = playerOperation(bl, ip, table_dic)
            #    #print(bl.players, bl.dealer)
            #    bl.playerOperation(ip, ope)

        #bl.checkStatus()
        #if bl.finish == 1:
    bl.dealerDraw()
    bl.dealerPointCal()
    bl.playerPoint()
    bl.finalScoreCal()

    #print("player hand")
    #print(bl.players)
    #print("dealer hand")
    #print(bl.dealer)
    #print("player bust")
    #print(bl.bust)
    #print("dealer bust")
    #print(bl.dealerBust)
    #print("player point")
    #print(bl.points)
    #print("dealer point")
    #print(bl.dealerPoint)
    #print("score")
    #print(bl.finalScore)
    #print("Number of cards")
    #print(len(bl.cards))

    finalScores.append(bl.finalScore)
    finalBets.append(bl.totalBetting)

# change to numpy array for calculation
finalScores = np.array(finalScores)
finalBets = np.array(finalBets)
print("average return per bet is %s"%(np.sum(finalScores)/np.sum(finalBets)))

n = len(finalScores)
win_number = np.sum(finalScores>0)
lose_number = np.sum(finalScores<0)
draw_number = np.sum(finalScores==0)

print("winning ratio %s, lose ratio%s, draw ratio%s"%(win_number/n, lose_number/n, draw_number/n))

returnScores = np.divide(finalScores, finalBets)
avg_return = np.average(returnScores)
std_return = np.std(returnScores)
print("average return is %s"%(avg_return))
print("standard deviation of return %s, std of absolute reward %s"%(std_return/np.sqrt(n), np.std(finalScores)/np.sqrt(n)))

print("sharp ratio %s"%(avg_return/std_return))
print("maximum return %s,  minimum return %s"%(np.max(returnScores), np.min(returnScores)))








