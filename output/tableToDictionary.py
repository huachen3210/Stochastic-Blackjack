__author__ = 'gecheng1219'


import pandas


def tableToDic(fileName):

    table = pandas.read_csv(fileName)

    col = list(table.columns.values)

    col.pop(0)

    row = list(table.iloc[:,0])


    dic = {}

    for i in range(len(row)):
        for j in range(len(col)):
            dic[str(row[i]) + ',' +  str(col[j])] = table.iloc[i][j+1]

    return dic