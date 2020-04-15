def cal_total_hand(current_value, new_card, type):
    tot_value =0
    if new_card != 1:
        tot_value = current_value + new_card
        type = "hard"
    elif new_card == 1 and current_value > 10:
        tot_value = current_value+new_card
        type = "hard"
    else:
        tot_value = current_value+11
        type = "soft"
    return tot_value, type
