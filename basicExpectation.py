__author__ = 'gecheng'

import time


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
                bustProb = dealerBustProb(d + i, 'hard') * (1/13 + (1/13)*(i==10)*3) + bustProb
            bustProb = bustProb + (1/13) * dealerBustProb(d + 11, 'soft')
        if d >= 11 and d <= 15:
            for i in range(1, 16 - d + 1):
                bustProb = dealerBustProb(d + i, 'hard') * (1/13) + bustProb
            bustProb = bustProb + (abs(10 - (21-d)) + 3) * (10 > (21-d))/13
        if d == 16:
            bustProb = (abs(10 - (21-d)) + 3) * (10 > (21-d))/13
    if type == 'soft':
        if d == 11:
            for i in range(1, 16-d+1):
                bustProb = dealerBustProb(d+i, 'soft') * (1/13) + bustProb

        if d >= 12 and d <= 15:
            for i in range(1, 16-d+1):
                bustProb = dealerBustProb(d+i, 'soft') * (1/13) + bustProb

            for j in range(21-d+1, 11):
                bustProb = bustProb + (1/13)*(1+(j==10)*3)*dealerBustProb(d+j-10, 'hard')
        if d == 16:
            for j in range(21-d+1, 11):
                bustProb = bustProb + (1/13)*(1+(j==10)*3)*dealerBustProb(d+j-10, 'hard')

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
                standingProb = (1/13 + (1/13)*(i==10)*3) * dealerStanding(d + i, g, 'hard') + standingProb
            standingProb = (1/13)*dealerStanding(d+11, g, 'soft') + standingProb
        if d >= 11 and d <= 16:
            for i in range(1,21 - d + 1):
                standingProb = (1/13 + (1/13)*(i==10)*3) * dealerStanding(d + i, g, 'hard') + standingProb
        if d >= 17 and d <= 21:
            if d == g:
                standingProb = 1
            else:
                standingProb = 0

    if type == 'soft':
        if d == 11:
            for i in range(2,11):
                standingProb = (1/13 + (1/13)*(i==10)*3) * dealerStanding(d + i, g, 'soft') + standingProb
            standingProb  =  (1/13)*dealerStanding(d+1, g, 'soft') + standingProb

        if d >= 12 and d <= 16:
            for i in range(1, 21 - d + 1):
                standingProb = (1/13 + (1/13)*(i==10)*3) * dealerStanding(d + i, g, 'soft') + standingProb

            for j in range(21-d+1,11):
                standingProb = (1/13 + (1/13)*(j==10)*3) * dealerStanding(d + j - 10, g, 'hard') + standingProb

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
    expectation = 0
    expectation = dealerBustProb(d, dtype) * 1 + expectation
    for j in range(17, 22):
        if j < p:
            expectation = dealerStanding(d, j, dtype) * 1 + expectation
        elif j > p:
            expectation = dealerStanding(d, j, dtype) * (-1) + expectation

    return expectation



### calculate the expectation value of hitting
##########################
# p: point of player
# d: point of dealer
# ptype : type of point for player        soft or hard
# type : type of point for dealer        soft or hard
##########################
def hitExpectation(p, d, ptype, dtype):
    expectation = 0
    if ptype == 'hard':
        if p <= 10:
            for i in range(2, 11):
                expectation = Expectation(p+i, d, 'hard', dtype) * ((1/13) + (1/13)*(i==10)*3) + expectation
            expectation = expectation + (1/13) * Expectation(p + 11, d, 'soft', dtype)
        if p >= 11:
            for i in range(1, 21-p+1):
                expectation = Expectation(p+i, d, 'hard', dtype) * ((1/13) + (1/13)*(i==10)*3) + expectation
            for i in range(21-p+1, 11):
                expectation = expectation + ((1/13) + (1/13)*(i==10)*3) * (-1)

    if ptype == 'soft':
        if p == 11:
            for i in range(1, 11):
                expectation = expectation + Expectation(p+i, d, 'soft', dtype) * ((1/13) + (1/13)*(i==10)*3)

        if p >= 12:
            for i in range(1, 21-p+1):
                expectation = expectation + Expectation(p+i, d, 'soft', dtype) * ((1/13) + (1/13)*(i==10)*3)
            for j in range(21-p+1, 11):
                expectation = Expectation(p+j-10, d, 'hard', dtype) * ((1/13) + (1/13)*(j==10)*3) + expectation
    return expectation




def Expectation(p, d, ptype, dtype):
    return max([hitExpectation(p, d, ptype, dtype), standingExpectation(p, d, ptype, dtype)])



### Example

s = time.time()

p = 14
d = 9
print(hitExpectation(p, d, 'hard', 'hard'))
print(standingExpectation(p, d, 'hard', 'hard'))


e = time.time()

print(e - s)

