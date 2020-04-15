__author__ = 'Huachen Ren'

import numpy as np
from utils import cal_total_hand
from basicExpectation import Expectation, standingExpectation, hitExpectation
P_next = 1/13


def E_double_hard(p, d, dtype):
    """
    Calculate the conditional expectation of choosing double

    :param p:
    :param d:
    :param ptype:
    :param dtype:
    :return:
    """
    expect=0
    for i in range(1, 11):
        p_update, type_update = cal_total_hand(p, i)
        expect+=standingExpectation(p_update, d, type_update, dtype)*P_next
    return expect







# Case1: Hard Hand, two initial diff cards


