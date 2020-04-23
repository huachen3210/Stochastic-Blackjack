import pandas as pd


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

def tableToDic(fileName):

    table = pd.read_csv(fileName)

    col = list(table.columns.values)

    col.pop(0)

    row = list(table.iloc[:,0])


    dic = {}

    for i in range(len(row)):
        for j in range(len(col)):
            dic[str(row[i]) + ',' +  str(col[j])] = table.iloc[i][j+1]

    return dic