# Intialize global tables to store expectations and strategy to avoid repeated calculation
################################################

import numpy as np
import pandas as pd

# possible values of player's initial value
card_value = [2,3,4,5,6,7,8,9,10,11]

# possible initial values for hard type, soft type and pair type
hard_player_value = list(range(4,22))
soft_player_value = list(range(12,22))
pair_value = [4,6,8,10,12,14,16,18,20,22]

# probability of draw next card

p_next = 1/13
global strat_dict
global expect_dict

# Initialize table to store the strategy
hard_strat_df = pd.DataFrame("0", columns=card_value, index=hard_player_value)
soft_strat_df = pd.DataFrame("0", columns=card_value, index=soft_player_value)
pair_strat_df = pd.DataFrame("0", columns=card_value, index=pair_value)
strat_dict = {"hard":hard_strat_df, "soft":soft_strat_df, "pair":pair_strat_df}


# Initilzie table to store expectation
hard_expect_df = pd.DataFrame(0, columns=card_value, index=hard_player_value)
soft_expect_df = pd.DataFrame(0, columns=card_value, index=soft_player_value)
pair_expect_df = pd.DataFrame(0, columns=card_value, index=pair_value)
standing_hard_expect_df = pd.DataFrame(0, columns=card_value, index=hard_player_value)
hit_hard_expect_df = pd.DataFrame(0, columns=card_value, index=hard_player_value)
standing_soft_expect_df = pd.DataFrame(0, columns=card_value, index=soft_player_value)
hit_soft_expect_df = pd.DataFrame(0, columns=card_value, index=soft_player_value)

expect_dict = {"hard":hard_expect_df, "soft":soft_expect_df, "pair":pair_expect_df,
               "hard_stand": standing_hard_expect_df, "hard_hit":hit_hard_expect_df,
               "soft_stand":standing_soft_expect_df, "soft_hit":hit_soft_expect_df}

# H for hit, S for stand, D for double, SP for split
strategy_list = ["H", "S", "D", "SP"]
