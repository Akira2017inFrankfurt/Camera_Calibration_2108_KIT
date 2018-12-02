# -*- coding: utf-8 -*-


"""
Created on 02 Dec 2018
@author: Huang
"""

import numpy as np
import math


def s_e_d(u1, u2, F):
    l_2 = np.dot(F, u1)
    l_1 = np.dot(F.T, u2)

    length_u2 = len(u2)
    ejs = []
    for i in range(length_u2):
        ejs.append(u2[i] * l_2[i])

    s_l_1_1 = l_1[::3]
    s_l_1_2 = l_1[1::3]
    s_l_2_1 = l_2[::3]
    s_l_2_2 = l_2[1::3]

    scales = []
    for j in range(len(s_l_1_1)):
        t_1 = pow(s_l_1_1[j], 2) + pow(s_l_1_2[j], 2)
        t_2 = pow(s_l_2_1[j], 2) + pow(s_l_2_2[j], 2)
        # todo: ensure the value of t_1 is not zero!
        scales.append(1.0 / math.sqrt(t_1) + 1.0 / math.sqrt(t_2))

    e = [sum(ejs) * value for value in scales]
