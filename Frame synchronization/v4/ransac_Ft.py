# -*- coding = utf-8 -*-

import random
import numpy as np
import cv2 as cv
from F_dt_8pt import F_dt_8pt
from inandout import writetofile
# from scipy import linalg


def affine_trans(matrix):
    matrix = matrix.T
    temp_matrix = np.ones((3, matrix.shape[1]))
    temp_matrix[0:2, :] = matrix
    return temp_matrix
'''
def err_fcn(u1, u2, F):

    u1 = affine_trans(u1)
    u2 = affine_trans(u2)

    Res_errfcn.write('\n u1  \n')
    s = str(u1)
    Res_errfcn.write(s)

    Res_errfcn.write('\n u2  \n')
    s = str(u2)
    Res_errfcn.write(s)

    l2 = np.dot(F , u1)
    l1 = np.dot(F.conj().T , u2)
    ejs = np.multiply( u2, l2)
    ejs = np.reshape(ejs, (ejs.shape[0]*ejs.shape[1], 1))

    Res_errfcn.write('\n ejs  \n')
    s = str(ejs)
    Res_errfcn.write(s)

    l11s = l1[0:len(l1):3]
    l12s = l1[1:len(l1):3]
    l21s = l2[0:len(l2):3]
    l22s = l2[1:len(l2):3]
    scales = 1 / np.sqrt(l11s ** 2 + l12s ** 2) + 1 / np.sqrt(l21s ** 2 + l22s ** 2)

    Res_errfcn.write('\n scales  \n')
    s = str(scales)
    Res_errfcn.write(s)

    temp = np.reshape(ejs, (3, ejs.shape[0] / 3))
    temp_sum = np.sum(temp, axis=0)

    Res_errfcn.write('\n temp_sum  \n')
    s = str(temp_sum)
    Res_errfcn.write(s)

    e = np.multiply( temp_sum, scales)

    Res_errfcn.write('\n err_fcn result  \n')
    s = str(e)
    Res_errfcn.write(s)

    Res_errfcn.close()

    return e
'''

def List2Mat(Matlist, nsample):
    temp_M = np.zeros((nsample, nsample))
    for i in range(temp_M.shape[1]):
        temp_M[:, i] = Matlist[i]
    Matlist = temp_M
    return Matlist


def ransac_Ft(u1, u2, interp_dist, thr, rounds):

    #clear the before txt data
    writefilename = str('result_ransac.txt')

    inliners_best = []
    emin = np.inf
    Ftres = 0
    dtres = 0
    
    n_samples = 8

    writetofile(interp_dist, str('inter_dist(step)  '), str('result_ransac.txt'))

    if interp_dist > 0:
        start = 0
        finish = u1.shape[0] - interp_dist
        u2next = u2[interp_dist: u2.shape[0], :]
        u2curr = u2[0: u2.shape[0] - interp_dist, :]
        u1curr = u1[0: u1.shape[0] - interp_dist, :]
    else:
        start = - interp_dist
        finish = u1.shape[0]
        u2curr = u2[-interp_dist: u2.shape[0], :]
        u2next = u2[0: interp_dist + u2.shape[0], :]
        u1curr = u1[-interp_dist: u1.shape[0], :]
    vv = u2next-u2curr
    u1curr = affine_trans(u1curr)

    writetofile(vv, str(' vv '), str('result_ransac.txt'))

    for i in range(rounds):
        sample =random.sample(range(finish-start),n_samples)
        for index in range(n_samples):
            sample[index] = sample[index] + start - 1

        writetofile(sample, str(' sample '), str('result_ransac.txt'))

        u1s = u1[sample, :]
        u2s = u2[sample, :]

        writetofile(u1s, str(' u1s  '), str('result_ransac.txt'))
        writetofile(u2s, str(' u2s '), str('result_ransac.txt'))

        sample_next = range(n_samples)

        # print 'initial sample_next', sample_next
        for index in range(n_samples):
            sample_next[index] = sample[index] + interp_dist

        v = u2[sample_next, :] - u2[sample, :]

        writetofile(v, str(' v '), str('result_ransac.txt'))

        '''
        Mat_1 = np.array( [ \
            u2s[:, 0] * u1s[:, 0], u2s[:, 0] * u1s[:, 1], u2s[:, 0], \
            u2s[:, 1] * u1s[:, 0], u2s[:, 1] * u1s[:, 1], u2s[:, 1], \
            u1s[:,0], u1s[:, 1], np.ones((1,n_samples)) \
            ] )

        Mat_2 = np.array( [ \
            v[:, 0] * u1s[:, 0], v[:, 0] * u1s[:, 1], v[:, 0], \
            v[:, 1] * u1s[:, 0], v[:, 0] * u1s[:, 1], v[:, 1], \
            np.zeros((1, n_samples)), np.zeros((1, n_samples)), np.zeros((1, n_samples)) \
            ] )

        Mat_1 = List2Mat(Mat_1,n_samples)
        Mat_2 = List2Mat(Mat_2,n_samples)

        # output
        Res_ransac.write('\n Mat_1  \n')
        s = str(Mat_1)
        Res_ransac.write(s)
        Res_ransac.write('\n Mat_2  \n')
        s = str(Mat_2)
        Res_ransac.write(s)

        
        invMat_2 = linalg.pinv(Mat_2)
        test_1 = np.dot(invMat_2, Mat_2)

        Res_ransac.write('\n invMat_2  \n')
        s = str(invMat_2)
        Res_ransac.write(s)

        Res_ransac.write('\n test_1 is invMat_2 *Mat_2  \n')
        s = str(test_1)
        Res_ransac.write(s)

        GEP_A =np.dot(invMat_2, Mat_1)

        Res_ransac.write('\n GEP_A  \n')
        s = str(GEP_A)
        Res_ransac.write(s)

        dt, F = linalg.eig(GEP_A)

        Res_ransac.write('\n dt  \n')
        s = str(dt)
        Res_ransac.write(s)

        Res_ransac.write('\n F  \n')
        s = str(F)
        Res_ransac.write(s)

        dt = - dt.real
        F = F.real

        Res_ransac.write('\n dt_real  \n')
        s = str(dt)
        Res_ransac.write(s)

        Res_ransac.write('\n F_real  \n')
        s = str(F)
        Res_ransac.write(s)

        temp_test =[]
        for index in range(9):
            temp_test.append(np.dot( ( Mat_1 + dt[index] * Mat_2 ), F[:, index] ))

        Res_ransac.write('\n temp_test  show  the estimation of beta and F is good or not \n')
        s = str(temp_test)
        Res_ransac.write(s)
        
        
        F_2= cv.findFundamentalMat(u1s, u2s, method=cv.FM_RANSAC)

        Res_ransac.write('\n  F_2  is \n')
        s = str(F_2)
        Res_ransac.write(s)

        temp_F_2 = np.reshape(F_2[0], (9,1))

        dt=np.zeros((1, n_samples))
        for index in range(n_samples):
            # print Mat_1[index], Mat_2[index] ,np.dot(Mat_1[index],  F_2)
            dt[:, index] = -np.dot(Mat_1[index] ,  temp_F_2)  / (np.sum(Mat_2[index ]))

        F = np.reshape(F_2[0], (3,3))
        '''

        F, dt = F_dt_8pt(u1s, u2s, v)

        if len(F) == 0:
            Res_ransac.write('\n F=0 appear  \n')
            continue

        det_temp = []
        #evaluate hypotheses
        for k in range(F.shape[0]):
            Fh = F[k]
            Fh = np.reshape(Fh, (3,3))

            writetofile(Fh, str(' Fh '), str('result_ransac.txt'))

            # for test error
            real_F = [[0.0000 , -0.0004  , 0.0348], [0.0004 , 0.0000 , -0.0937], [-0.0426 ,0.0993,   0.9892]]
            error_F = (Fh-real_F)**2
            sum_error = np.sum(error_F)

            writetofile(error_F, str(' error_F '), str('result_ransac.txt'))
            writetofile(sum_error, str(' sum of error _F  '), str('result_ransac.txt'))

            # for test whether the Fh satisfy det(F) ~= 0
            #det_temp.append(np.linalg.det(Fh))
            #print 'det_temp is ', det_temp[-1]

            dth = dt[k]

            writetofile(dth, str(' dth '), str('result_ransac.txt'))


            if np.absolute(dth) > 10 :
                writetofile(dth ,str('dth  is too large '), writefilename)
                continue

            u2dt = u2curr + dth*vv

            # Res_errfcn = open('result_errfcn.txt', 'w')

            u2dt = affine_trans(u2dt)

            inliners = []
            e = 0
            Res_ransac = open(writefilename, 'a')
            Res_ransac.write('\n ejs  \n')

            for index in range(u1curr.shape[1]):
                #print 'u1curr is ', u1curr[ :, index]
                #print 'u2dt[index, :]', u2dt[ :, index]
                temp_ejs = cv.sampsonDistance(u1curr[ :, index], u2dt[:, index], Fh)
                ejs = np.absolute(temp_ejs)

                Res_ransac.write(', ')
                s = str(ejs)
                Res_ransac.write(s)

                if ejs < thr :
                    inliners.append(index)
                    e = e + ejs
            Res_ransac.close()

            writetofile(inliners, str(' inliners with threshold '), str('result_ransac.txt'))
            writetofile(len(inliners), str(' inliners length '), str('result_ransac.txt'))
            writetofile(e, str(' e '), str('result_ransac.txt'))

            #found better candidate
            if len(inliners) > len(inliners_best) or ( len(inliners) == len(inliners_best) and e < emin):

                writetofile(inliners, str('  better result appears  and new inliners  '), str('result_ransac.txt'))
                writetofile(len(inliners), str(' new inliners  length  '), str('result_ransac.txt'))

                Ftres =Fh
                dtres = dth
                emin = e
                inliners_best = inliners

                writetofile(dtres, str(' new dtres '), str('result_ransac.txt'))
                writetofile(Ftres, str(' new Ftres '), str('result_ransac.txt'))

                Res_ransac = open(writefilename, 'a')
                Res_ransac.write('\n end of the if   \n')
                Res_ransac.close()
    Res_ransac = open(writefilename, 'a')
    Res_ransac.write('\n end of the for loop    \n')
    Res_ransac.close()
    return Ftres, dtres,  inliners_best, emin





