__author__ = ['gecheng', "Huachen Ren"]

import time
from MyDataBase import *

### calculate bust probability of dealer
##########################
# d: point of dealer
# type : type of point for dealer     soft or hard
##########################
def dealerBustProb(d, type):
    bustProb = 0
    if type == 'hard':
        if d <= 10:
            for i in range(2, 11):
                bustProb = dealerBustProb(d + i, 'hard') * trans_prob[i-1] + bustProb
            bustProb = bustProb + trans_prob[0] * dealerBustProb(d + 11, 'soft')
        if d >= 11 and d <= 16:
            for i in range(1, 16 - d + 1):
                bustProb = dealerBustProb(d + i, 'hard') * trans_prob[i-1] + bustProb
            for i in range(11):
                if d+i>21:
                    bustProb += trans_prob[i-1]
            #bustProb = bustProb + (abs(10 - (21-d)) + 3) * (10 > (21-d))/13
        # if d == 16:
        #     bustProb = (abs(10 - (21-d)) + 3) * (10 > (21-d))/13
    if type == 'soft':
        if d == 11:
            for i in range(1, 16-d+1):
                bustProb = dealerBustProb(d+i, 'soft') * trans_prob[i-1] + bustProb

        if d >= 12 and d <= 15:
            for i in range(1, 16-d+1):
                bustProb = dealerBustProb(d+i, 'soft') * trans_prob[i-1] + bustProb

            for j in range(21-d+1, 11):
                bustProb = bustProb + trans_prob[j-1]*dealerBustProb(d+j-10, 'hard')
        if d == 16:
            for j in range(21-d+1, 11):
                bustProb = bustProb + trans_prob[j-1]*dealerBustProb(d+j-10, 'hard')

    return bustProb



### calculate the probability of dealer standing each point from 17 to 21
##########################
# d: point of dealer
# g: a value from 17 to 21
# type : type of point for dealer    soft or hard
##########################
def dealerStanding(d, g, type):
    standingProb = 0
    if type == 'hard':
        if d <= 10:
            for i in range(2,11):
                standingProb = trans_prob[i-1] * dealerStanding(d + i, g, 'hard') + standingProb
            standingProb = trans_prob[0]*dealerStanding(d+11, g, 'soft') + standingProb
        if d >= 11 and d <= 16:
            for i in range(1,21 - d + 1):
                standingProb = trans_prob[i-1] * dealerStanding(d + i, g, 'hard') + standingProb
        if d >= 17 and d <= 21:
            if d == g:
                standingProb = 1
            else:
                standingProb = 0

    if type == 'soft':
        if d == 11:
            for i in range(2,11):
                standingProb = trans_prob[i-1] * dealerStanding(d + i, g, 'soft') + standingProb
            standingProb  =  trans_prob[0]*dealerStanding(d+1, g, 'soft') + standingProb

        if d >= 12 and d <= 16:
            for i in range(1, 21 - d + 1):
                standingProb = trans_prob[i-1] * dealerStanding(d + i, g, 'soft') + standingProb

            for j in range(21-d+1,11):
                standingProb = trans_prob[j-1] * dealerStanding(d + j - 10, g, 'hard') + standingProb

        if d >= 17 and d <= 21:
            if d == g:
                standingProb = 1
            else:
                standingProb = 0

    return standingProb




### calculate the expectation value of standing
##########################
# p: point of player
# d: point of dealer
# ptype : type of point for player        soft or hard
# type : type of point for dealer        soft or hard
##########################
def standingExpectation(p, d, ptype, dtype):
    # check whether the expecation was computed
    if expect_dict[ptype+"_stand"].loc[p, d] == 0:
        expectation = 0
        expectation = dealerBustProb(d, dtype) * 1 + expectation
        for j in range(17, 22):
            if j < p:
                expectation = dealerStanding(d, j, dtype) * 1 + expectation
            elif j > p:
                expectation = dealerStanding(d, j, dtype) * (-1) + expectation
        expect_dict[ptype + "_stand"].loc[p, d] = expectation
        return expectation

    else:
        return expect_dict[ptype+"_stand"].loc[p, d]

def BJ_standingExpectation(d, dtype):
    """
    Calculate expectation after the player get blackjack and stand
    """
    expectation = 0
    expectation = dealerBustProb(d, dtype) * 1.5 + expectation
    for j in range(17, 21):
        expectation = dealerStanding(d, j, dtype) * 1.5 + expectation
    return expectation



### calculate the expectation value of hitting
##########################
# p: point of player
# d: point of dealer
# ptype : type of point for player        soft or hard
# type : type of point for dealer        soft or hard
##########################
def hitExpectation(p, d, ptype, dtype):
    # check whether the expecation was computed
    if expect_dict[ptype+"_hit"].loc[p, d] == 0:
        expectation = 0
        if ptype == 'hard':
            if p <= 10:
                for i in range(2, 11):
                    expectation = expect_dict["hard"].loc[p+i, d] * trans_prob[i-1] + expectation
                expectation = expectation + trans_prob[0] * expect_dict["soft"].loc[p + 11, d]
            if p >= 11:
                for i in range(1, 21-p+1):
                    expectation = expect_dict["hard"].loc[p+i, d] * trans_prob[i-1] + expectation
                for i in range(21-p+1, 11):
                    expectation = expectation + trans_prob[i-1] * (-1)

        if ptype == 'soft':
            if p == 11:
                for i in range(1, 11):
                    expectation = expectation + expect_dict["soft"].loc[p+i, d] * trans_prob[i-1]

            if p >= 12:
                for i in range(1, 21-p+1):
                    expectation = expectation + expect_dict["soft"].loc[p+i, d] * trans_prob[i-1]
                for j in range(21-p+1, 11):
                    expectation = expect_dict["hard"].loc[p+j-10, d] * trans_prob[j-1] + expectation
        expect_dict[ptype + "_hit"].loc[p, d] = expectation
        return expectation
    else:
        return expect_dict[ptype+"_hit"].loc[p, d]


def doubleExpectation(p, d, ptype, dtype):
    expectation = 0
    if ptype == "hard":
        # not bust
        for i in range(2, min(21-p+1, 11)):
            expectation += 2*standingExpectation(p+i, d, ptype, dtype)*trans_prob[i-1]
        # get A, convert to soft
        if p<=10:
            expectation += 2*standingExpectation(p+11, d, "soft", dtype)*trans_prob[0]
        # get A, hard
        elif p<21:
            expectation += 2*standingExpectation(p+1, d, ptype, dtype)*trans_prob[0]
        # bust
        for i in range(min(21-p+1, 11), 11):
            expectation += -2*trans_prob[i-1]
    else:
        # Since When only have one A, you can't choose double, we don't consider p=11
        for i in range(1, 21 - p + 1):
            expectation += 2*standingExpectation(p + i, d, ptype, dtype) * trans_prob[i-1]
        for j in range(21 - p + 1, 11):
            expectation += 2*standingExpectation(p + j - 10, d, 'hard', dtype) * trans_prob[j-1]
    return expectation



def splitExpectation(p, d, ptype, dtype):
    expectation = 0
    if ptype == "soft":
        # If split 2 A, then must get one more card and stand
        for j in range(1, 11):
            if j == 10:
                expectation += BJ_standingExpectation(d, dtype)*trans_prob[9]
            else:
                expectation += standingExpectation(11+j, d, ptype, dtype)*trans_prob[j-1]
    elif p == 20:
        for i in range(1, 11):
            if i == 1:
                expectation += BJ_standingExpectation(d, dtype)*trans_prob[0]
            else:
                expectation += expect_dict["hard"].loc[10+i, d]*trans_prob[i-1]
    else:
        for i in range(1, 11):
            if i == 1:
                expectation += expect_dict["soft"].loc[int(p / 2)+11, d]*trans_prob[i-1]
            else:
                expectation += expect_dict["hard"].loc[int(p / 2)+i, d]*trans_prob[i-1]

    return 2*expectation

def Expectation(p, d, ptype, dtype):
    # check whether the strategy was computed
    if strat_dict[ptype].loc[p, d] == "0":
        # First check whether expectation exists. If not
        # Compute hit expectation and stand expectation
        if expect_dict[ptype+"_hit"].loc[p, d] == 0:
            # have not calculate hit expectation
            hit_expect = hitExpectation(p, d, ptype, dtype)
            expect_dict[ptype+"_hit"].loc[p, d] = hit_expect

        else:
            hit_expect = expect_dict[ptype+"_hit"].loc[p, d]

        if expect_dict[ptype+"_stand"].loc[p, d] == 0:
            # have not calculate stand expectation
            stand_expect = standingExpectation(p, d, ptype, dtype)
            expect_dict[ptype+"_stand"].loc[p, d] = stand_expect
        else:
            stand_expect = expect_dict[ptype+"_stand"].loc[p, d]

        # choose optimal action
        if hit_expect > stand_expect:
            expect = hit_expect
            # update strategy table
            strat_dict[ptype].loc[p, d] = "H"
        else:
            expect = stand_expect
            strat_dict[ptype].loc[p, d] = "S"
        # update expectation table
        expect_dict[ptype].loc[p, d] = expect
        return expect
    else:
        return expect_dict[ptype].loc[p, d]



    #return max([hitExpectation(p, d, ptype, dtype), standingExpectation(p, d, ptype, dtype)])

if __name__ == "__main__":

    s = time.time()

    p = 13
    d = 11
    double_ind = False
    split_ind = False
    ptype = "hard"
    dtype = "soft"
    print("hit expectation is ", hitExpectation(p, d, ptype, dtype))
    print("stand expectation is ", standingExpectation(p, d, ptype, dtype))
    if double_ind:
        print("double expectation is ", doubleExpectation(p, d, ptype, dtype))
    if split_ind:
        print("split expectation is ", splitExpectation(p, d, ptype, dtype))

    print("strategy table")
    print(strat_dict[ptype])
    #print("pair table")

    print("expect table")
    print(expect_dict[ptype])


    e = time.time()
    print("code running time is %s" %(e - s))

