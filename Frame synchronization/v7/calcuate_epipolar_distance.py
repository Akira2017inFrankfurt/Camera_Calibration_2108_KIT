#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 02 Dec 2018
@author: Huang
"""

import numpy as np
import math

def s_e_d(u1, u2, F):
    l_2 = np.dot(F, u1)
    l_1 = np.dot(F.conj().T, u2)

    u_2_reshape = np.reshape(u2.conj().T, (len(u2) * len(u2[0]), 1))
    l_2_reshape = np.reshape(l_2.conj().T, (len(l_2) * len(l_2[0]), 1))

    length_u_2 = len(u_2_reshape)

    ejs = []
    for i in xrange(length_u_2):
        ejs.append(u_2_reshape[i] * l_2_reshape[i])

    s_l_1_1 = l_1[0]
    s_l_1_2 = l_1[1]
    s_l_2_1 = l_2[0]
    s_l_2_2 = l_2[1]

    scales = []

    for j in xrange(len(s_l_1_1)):
        t_1 = pow(s_l_1_1[j], 2) + pow(s_l_1_2[j], 2)
        t_2 = pow(s_l_2_1[j], 2) + pow(s_l_2_2[j], 2)
        # todo: ensure the value of t_1 is not zero!
        scales.append(1.0 / math.sqrt(t_1) + 1.0 / math.sqrt(t_2))

    temp = np.reshape(ejs, ((length_u_2 / 3),3) )
    temp = temp.T

    e = []
    for col_index in xrange(len(u_2_reshape) / 3):
        sum = 0
        sum = temp[0][col_index] + temp[1][col_index] + temp[2][col_index]
        e.append(sum * scales[col_index])
    return e

