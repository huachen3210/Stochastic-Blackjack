import pandas as pd
import numpy as np
from basicExpectation import dealerStanding, dealerBustProb
card_value = ["A",2,3,4,5,6,7,8,9,10]
# possible values of player's initial value
p_initial_value = range(5,22)


# Initialize table to store the strategy
strat_df = pd.DataFrame(columns=["A",2,3,4,5,6,7,8,9,10], index=range(5,22))
# If initial value is 21, then stand
strat_df.loc[21:] = "S"

# Initialize table to store the conditional expectation for each action

# total bet
def standingExpectation(p, d, ptype, dtype):
    expectation = 0
    dealer_bust_prob = dealerBustProb(d, dtype)
    # Calculate standing expectation when p's value is 21
    if p==21:
        dealer_stand_prob = 0
        for i in range(17, 21):
            dealer_stand_prob += dealerStanding(d, i, dtype)
        # Player get BJ
        expectation = 1.5* (dealer_bust_prob+dealer_stand_prob)

    else:

        expectation = dealer_bust_prob * 1 + expectation
        for j in range(17, 22):
            if j < p:
                expectation = dealerStanding(d, j, dtype) * 1 + expectation
            elif j > p:
                expectation = dealerStanding(d, j, dtype) * (-1) + expectation


    return expectation



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
    if p == 21:
        return
    return max([hitExpectation(p, d, ptype, dtype), standingExpectation(p, d, ptype, dtype)])


# Case 1: Hard, no pair
def Search_opt_strat(ptype, dtype):
    for d in card_value:
        for p0 in list(p_initial_value)[::-2]:

            h_expec = hitExpectation(p0, d, ptype, dtype)
            s_expec = standingExpectation(p0, d, ptype, dtype)
            d_expec = DoubleExpectation(p0, d, ptype, dtype)
            #Sp_expec = Sp_Expect(p0, d, ptype, dtype)
            max_id = np.argmax([h_expec, s_expec, d_expec])
            if max_id == 0:
                strat_df.loc[p0, d] = "H"
            elif max_id == 1:
                strat_df.loc[p0, d] = "S"
            else:
                strat_df.loc[p0, d] = "D"


