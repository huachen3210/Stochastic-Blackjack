__author__ = 'Huachen Ren'

import os
import time
from MyDataBase import *
from basicExpectation import doubleExpectation, splitExpectation, standingExpectation, hitExpectation


# When search strategy, should follow the order of hard, soft and pair
def Search_opt_strat(ptype, pair_ind, trans_prob, silence=False):
    """
    Iterate all possible combinations of player card and dealer card and
    compute expectation and find the optimal strategy

    :param ptype: player's card type
    :param pair_ind: dealer's card type
    """
    if pair_ind != "pair" and ptype == "hard":
        p_initial_value = hard_player_value
    elif pair_ind != "pair" and ptype == "soft":
        p_initial_value = soft_player_value
    else:
        p_initial_value = pair_value
    for d in card_value:
        if d == 11:
            dtype = "soft"
        else:
            dtype = "hard"

        # p0 is the total card value. For AA case, p0=22. p_initial means player's starting value
        # for un-spliting case, so p_initial=12.
        for p0 in p_initial_value[::-1]:
            if not silence:
                print("Begin to calculate strategy for (%s, %s, %s, %s, %s)"%(p0, d, ptype, dtype, pair_ind))
            if pair_ind == "pair" and p0 == 22:
                p_initial = 12
                ptype = "soft"
            elif pair_ind == "pair" and p0 < 22:
                ptype = "hard"
                p_initial = p0
            else:
                p_initial = p0
            # Calculate expectation for each action
            h_expect = hitExpectation(p_initial, d, ptype, dtype, trans_prob)
            s_expect = standingExpectation(p_initial, d, ptype, dtype, trans_prob)
            d_expect = doubleExpectation(p_initial, d, ptype, dtype, trans_prob)
            if pair_ind == "pair":
                expect_list = [h_expect, s_expect, d_expect, splitExpectation(p0, d, ptype, dtype, trans_prob)]
            else:
                expect_list = [h_expect, s_expect, d_expect]
            # Compute the maximum expectation
            max_id = np.argmax(expect_list)
            # Save strategy and expect into table
            if pair_ind == "pair":
                strat_dict["pair"].loc[p0, d] = strategy_list[max_id]
                expect_dict["pair"].loc[p0, d] = expect_list[max_id]
            else:
                strat_dict[ptype].loc[p_initial, d] = strategy_list[max_id]
                expect_dict[ptype].loc[p_initial, d] = expect_list[max_id]
            if not silence:
                print("Optimal Strategy for (%s, %s, %s, %s) is %s with expectation %s"%(p0, d, ptype, dtype, strategy_list[max_id], expect_list[max_id]))


if __name__ == "__main__":
    s = time.time()
    # Probability of drawing 10, 11, 12, or 13
    p_10 = 4/13
    # probability of drawing each value
    trans_prob = [(1 - p_10) / 9] * 9 + [p_10]

    ptype = "hard"
    pair_ind = "not pair"
    Search_opt_strat(ptype, pair_ind, trans_prob)
    ptype = "soft"
    Search_opt_strat(ptype, pair_ind, trans_prob)
    pair_ind = "pair"
    Search_opt_strat(ptype, pair_ind, trans_prob)

    print("#######################################################")
    print("hard strategy table")
    print(strat_dict["hard"])

    print("hard expect table")
    print(expect_dict["hard"])
    print("#######################################################")

    print("soft strategy table")
    print(strat_dict["soft"])

    print("soft expect table")
    print(expect_dict["soft"])
    print("#######################################################")


    print("pair strategy table")
    print(strat_dict["pair"])

    print("pair expect table")
    print(expect_dict["pair"])

    print("#######################################################")

    if not os.path.exists("./output"):
        os.makedirs("./output")

    print("Begin to write table")
    # hard_table = pd.concat([strat_dict["hard"], expect_dict["hard"]]).to_csv("output/hard_table.csv")
    # soft_table = pd.concat([strat_dict["soft"], expect_dict["soft"]]).to_csv("output/soft_table.csv")
    # pair_table = pd.concat([strat_dict["pair"], expect_dict["pair"]]).to_csv("output/pair_table.csv")
    strat_dict["hard"].to_csv("output/hard_table.csv")
    strat_dict["soft"].to_csv("output/soft_table.csv")
    strat_dict["pair"].to_csv("output/pair_table.csv")

    # expect_dict["hard_hit"].to_csv("output/hard_hit_expectation.csv")
    # expect_dict["hard_stand"].to_csv("output/hard_stand_expectation.csv")
    # expect_dict["soft_hit"].to_csv("output/soft_hit_expectation.csv")
    # expect_dict["soft_stand"].to_csv("output/soft_stand_expectation.csv")

    e = time.time()
    print("code running time is %s" %(e - s))
