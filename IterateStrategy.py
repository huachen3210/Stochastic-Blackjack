__author__ = 'Huachen Ren'

import os
import time
from MyDataBase import *
from Strategy import Search_opt_strat
#begin_p10 = 0.2
#end_p10 = 0.34
#step_size = 0.01
range_10 =[0.2]
#range_10 = np.concatenate([range_10, np.array([4/13])])

s = time.time()

for i in range_10:
    p_10 = i
    trans_prob = [(1 - p_10) / 9] * 9 + [p_10]
    print("Begin to calculate strategy of 10 ratio %s"%p_10)

    ptype = "hard"
    pair_ind = "not pair"
    Search_opt_strat(ptype, pair_ind, trans_prob, True)
    ptype = "soft"
    Search_opt_strat(ptype, pair_ind, trans_prob, True)
    pair_ind = "pair"
    Search_opt_strat(ptype, pair_ind, trans_prob, True)
    output_folder = "./output/output_"+str(i)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print("Begin to write table")
    # hard_table = pd.concat([strat_dict["hard"], expect_dict["hard"]]).to_csv("output/hard_table.csv")
    # soft_table = pd.concat([strat_dict["soft"], expect_dict["soft"]]).to_csv("output/soft_table.csv")
    # pair_table = pd.concat([strat_dict["pair"], expect_dict["pair"]]).to_csv("output/pair_table.csv")
    strat_dict["hard"].to_csv(os.path.join(output_folder, "hard_table_%s.csv"%p_10))
    strat_dict["soft"].to_csv(os.path.join(output_folder, "soft_table_%s.csv"%p_10))
    strat_dict["pair"].to_csv(os.path.join(output_folder, "pair_table_%s.csv"%p_10))


e = time.time()
print("code running time is %s" %(e - s))