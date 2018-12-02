# -*- coding: utf-8 -*-


"""
Created on 02 Dec 2018
@author: Huang
"""

import numpy as np
import math


def s_e_d(u1, u2, F):
    # 3 * 80
    l_2 = np.dot(F, u1)
    # 3 * 80
    l_1 = np.dot(F.T, u2)

    # 3 * 80 = 240 * 1
    u_2_reshape = np.reshape(u2.T, (len(u2) * len(u2[0]), 1))
    l_2_reshape = np.reshape(l_2.T, (len(l_2) * len(l_2[0]), 1))

    # 240
    length_u_2 = len(u_2_reshape)

    # 240 * 1
    ejs = []
    for i in range(length_u_2):
        ejs.append(u_2_reshape[i] * l_2_reshape[i])

    # 1 * 80
    # s_l_1_1 就是l_1的第一行
    s_l_1_1 = l_1[0]
    s_l_1_2 = l_1[1]
    s_l_2_1 = l_2[0]
    s_l_2_2 = l_2[1]

    # 1 * 80
    scales = []
    for j in range(len(s_l_1_1)):
        t_1 = pow(s_l_1_1[j], 2) + pow(s_l_1_2[j], 2)
        t_2 = pow(s_l_2_1[j], 2) + pow(s_l_2_2[j], 2)
        # todo: ensure the value of t_1 is not zero!
        scales.append(1.0 / math.sqrt(t_1) + 1.0 / math.sqrt(t_2))

    temp = np.reshape(ejs, (3, length_u_2 / 3))

    # 取列的和，然后做乘运算，得到结果加入到e中
    e = []
    for col_index in range(len(u_2_reshape) / 3):
        sum = 0
        sum = temp[0][col_index] + temp[1][col_index] + temp[2][col_index]
        e.append(sum * scales[col_index])

    return e
