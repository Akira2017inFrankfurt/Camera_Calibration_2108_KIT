# -*- coding: utf-8 -*-


"""
Created on 02 Dec 2018
@author: Huang
"""

import numpy as np
import math


# for test
'''''
from inandout import errortest
from inandout import test
filepath = r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\u1.txt'
test_u1 = test(filepath, float)
test_u1 = np.reshape(test_u1,(3,5836))
filepath = r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\u2.txt'
test_u2 = test(filepath, float)
test_u2 = np.reshape(test_u2,(3,5836))
filepath = r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\F.txt'
test_F = test(filepath, float)
test_F = np.reshape(test_F,(3,3))
'''

def s_e_d(u1, u2, F):
    # 3 * 80
    l_2 = np.dot(F, u1)
    # 3 * 80
    l_1 = np.dot(F.conj().T, u2)

    # 3 * 80 = 240 * 1
    u_2_reshape = np.reshape(u2.conj().T, (len(u2) * len(u2[0]), 1))
    l_2_reshape = np.reshape(l_2.conj().T, (len(l_2) * len(l_2[0]), 1))

    # 240
    length_u_2 = len(u_2_reshape)

    # 240 * 1
    ejs = []
    for i in range(length_u_2):
        ejs.append(u_2_reshape[i] * l_2_reshape[i])

    temp_M = np.zeros(( len(ejs),1))
    for i in range(temp_M.shape[0]):
        temp_M[i] = ejs[i]
    ejs_test = temp_M

   # errortest(ejs_test, 'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\ejs.txt', float, False)

    s_l_1_1 = l_1[0]
    s_l_1_2 = l_1[1]
    s_l_2_1 = l_2[0]
    s_l_2_2 = l_2[1]

    # for test
    '''''
    errortest(s_l_1_1, 'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\l11s.txt', float,False)
    errortest(s_l_1_2, 'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\l12s.txt',float,False)
    errortest(s_l_2_1, 'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\l21s.txt',float,False)
    errortest(s_l_2_2, 'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\l22s.txt',float,False)
    '''

    scales = []
    #for j in range(len(s_l_1_1)):
    for j in range(len(s_l_1_1)):
        t_1 = pow(s_l_1_1[j], 2) + pow(s_l_1_2[j], 2)
        t_2 = pow(s_l_2_1[j], 2) + pow(s_l_2_2[j], 2)
        # todo: ensure the value of t_1 is not zero!
        scales.append(1.0 / math.sqrt(t_1) + 1.0 / math.sqrt(t_2))

    # for test
    '''''
    temp_M = np.zeros((len(scales),1))
    for i in range(temp_M.shape[0]):
        temp_M[i] = scales[i]
    scales_test = temp_M
    errortest(scales_test, 'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\scale.txt', float, False)
    '''''
    temp = np.reshape(ejs, ((length_u_2 / 3),3) )
    temp = temp.T

    # 取列的和，然后做乘运算，得到结果加入到e中
    e = []
    for col_index in range(len(u_2_reshape) / 3):
        sum = 0
        sum = temp[0][col_index] + temp[1][col_index] + temp[2][col_index]
        e.append(sum * scales[col_index])
    return e

# for test
'''''
Res = open('error.txt', 'w')
e = s_e_d(test_u1, test_u2,test_F)

temp_M = np.zeros((len(e),1))
for i in range(temp_M.shape[0]):
    temp_M[i] = e[i]
e_test = temp_M

errortest(e_test, 'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\e.txt',float, False )
Res.close()
'''