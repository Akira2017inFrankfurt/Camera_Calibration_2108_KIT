# -*- coding = utf-8 -*-

import random
import numpy as np
from F_dt_8pt import F_dt_8pt
from calcuate_epipolar_distance import s_e_d

# for test
from inandout import writetofile
from inandout import test


def affine_trans(matrix):
	matrix = matrix.T
	temp_matrix = np.ones((3, matrix.shape[1]))
	temp_matrix[0:2, :] = matrix
	return temp_matrix


def List2Mat(Matlist, nsample):
	temp_M = np.zeros((nsample, nsample))
	for i in range(temp_M.shape[1]):
		temp_M[:, i] = Matlist[i]
	Matlist = temp_M
	return Matlist


def ransac_Ft(u1, u2, interp_dist, thr, rounds):

	#clear the before txt data
	Res = open('result_solver.txt', 'w')
	Res.close()

	writefilename = str('result_ransac_Ft.txt')

	inliners_best = []
	emin = np.inf
	Ftres = 0
	dtres = 0

	n_samples = 8

	writetofile(interp_dist, str('inter_dist(step)  '), writefilename)

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

	# for test use sample in matlab

	''''
	writetofile(vv, str(' vv '), writefilename)
	filepath_sample= r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\sample.txt'
	mat_sample = test(filepath_sample, int)
	mat_sample = np.reshape(mat_sample, (len(mat_sample)/8, 8))
	'''

	for i in range(rounds):

		#when not need to compare with matlab, aktive the unter annotation
		sample =random.sample(range(finish-start),n_samples)

		# sample = mat_sample[i]
		for index in range(n_samples):
			sample[index] = sample[index] + start - 1

		#writetofile(sample, str(' sample '), writefilename)

		u1s = u1[sample, :]
		u2s = u2[sample, :]

		#writetofile(u1s, str(' u1s  '), writefilename)
		#writetofile(u2s, str(' u2s '), writefilename)

		sample_next = range(n_samples)

		# print 'initial sample_next', sample_next
		for index in range(n_samples):
			sample_next[index] = sample[index] + interp_dist

		v = u2[sample_next, :] - u2[sample, :]

		#writetofile(v, str(' v '), writefilename)

		F, dt = F_dt_8pt(u1s, u2s, v)

		if len(F) == 0:
			Res = open('result_ransac_Ft.txt', 'a')
			Res.write('\n F=0 appear  \n')
			Res.close()
			continue

		#evaluate hypotheses

		for k in range(F.shape[0]):
			Fh = F[k]
			Fh = np.reshape(Fh, (3,3))

			writetofile(Fh, str(' Fh '), writefilename)

			# for test error
			'''
			real_F = [[0.0000 , -0.0004  , 0.0348], [0.0004 , 0.0000 , -0.0937], [-0.0426 ,0.0993,   0.9892]]
			error_F = (Fh-real_F)**2
			sum_error = np.sum(error_F)

			writetofile(error_F, str(' error_F '), writefilename)
			writetofile(sum_error, str(' sum of error _F  '), writefilename)
			'''

			dth = dt[k]

			writetofile(dth, str(' dth '), writefilename)


			if np.absolute(dth) > 50 :
				writetofile(dth, str('dth  is too large, go to next round '), writefilename)
				continue


			u2dt = u2curr + dth*vv
			u2dt = affine_trans(u2dt)

			inliners = []
			e = 0

			# in matlab use Fh' ,but in here we calculate Fh after reshape is just like Fh' in matlab, so no more need to transposition
			ejs = s_e_d(u1curr, u2dt, Fh)
			ejs = np.absolute(ejs)
			for index in range(len(ejs)):
				if ejs[index] < thr:
					inliners.append(index)
					e = e + ejs[index]

			# writetofile(inliners, str(' inliners with threshold '), writefilename)
			writetofile(len(inliners), str(' inliners length '), writefilename)
			writetofile(e, str(' e '), writefilename)

			#found better candidate
			if len(inliners) > len(inliners_best) or (len(inliners) == len(inliners_best) and e < emin):

				#writetofile(inliners, str('  better result appears  and new inliners  '), writefilename)
				writetofile(len(inliners), str(' new inliners  length  '), writefilename)

				Ftres =Fh
				dtres = dth
				emin = e
				inliners_best = inliners

				writetofile(dtres, str(' new dtres '), writefilename)
				writetofile(Ftres, str(' new Ftres '), writefilename)

				Res = open(writefilename, 'a')
				Res.write('\n end of the if   \n')
				Res.close()
	Res = open(writefilename, 'a')
	Res.write('\n end of the for loop    \n')
	Res.close()
	return Ftres, dtres,  inliners_best, emin





