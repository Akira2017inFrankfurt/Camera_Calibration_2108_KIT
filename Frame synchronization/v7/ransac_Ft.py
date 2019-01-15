#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 14 Jan 2019
@author: Hongliang (xmuhhl@outlook.com)
"""

import random
import numpy as np
from F_dt_8pt import F_dt_8pt
from calcuate_epipolar_distance import symmetric_epipolar_distance

# for test
from inandout import writetofile

def affine_transformation(matrix):
	matrix = matrix.T
	temp_matrix = np.ones((3, matrix.shape[1]))
	temp_matrix[0:2, :] = matrix
	return temp_matrix

def List2Mat(Matlist, nsample):
	temp_M = np.zeros((nsample, nsample))
	for i in xrange(temp_M.shape[1]):
		temp_M[:, i] = Matlist[i]
	Matlist = temp_M
	return Matlist

def ransac_Ft(u1, u2, interp_dist, thr, rounds, debug = False):

	#clear the before txt data
	#Res = open('result_solver.txt', 'w')
	#Res.close()
	if debug:
		writefilename = str('result_ransac_Ft.txt')

	inliners_best = []
	e_min = np.inf
	Ftres = 0
	dtres = 0

	n_samples = 8
	if debug:
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
	u1curr = affine_transformation(u1curr)

	for i in xrange(rounds):

		#when not need to compare with matlab, aktive the unter annotation
		sample =random.sample(range(finish-start),n_samples)

		# sample = mat_sample[i]

		for index in xrange(n_samples):
			sample[index] = sample[index] + start - 1

		#writetofile(sample, str(' sample '), writefilename)

		u1s = u1[sample, :]
		u2s = u2[sample, :]

		#writetofile(u1s, str(' u1s  '), writefilename)
		#writetofile(u2s, str(' u2s '), writefilename)

		sample_next = range(n_samples)

		# print 'initial sample_next', sample_next
		for index in xrange(n_samples):
			sample_next[index] = sample[index] + interp_dist

		v = u2[sample_next, :] - u2[sample, :]

		#writetofile(v, str(' v '), writefilename)

		F, dt = F_dt_8pt(u1s, u2s, v)

		if len(F) == 0:
			#Res = open('result_ransac_Ft.txt', 'a')
			#Res.write('\n F=0 appear  \n')
			#Res.close()
			continue

		if debug:
			if ~(len(dt) == 0):
				Res = open('dt.txt', 'a')
				col = len(dt)
				for i in xrange(col):
					s = str(dt[i])
					Res.write(s)
					Res.write('\n')
				Res.close()

		#evaluate hypotheses

		for k in xrange(F.shape[0]):
			Fh = F[k]
			Fh = np.reshape(Fh, (3,3))

			if debug:
				writetofile(Fh, str(' Fh '), writefilename)


			dth = dt[k]

			if debug:
				writetofile(dth, str(' dth '), writefilename)


			if np.absolute(dth) > 100 or np.absolute(dth) < 0.0001:
				if debug:
					writetofile(dth, str('dth  is too large, go to next round '), writefilename)
				continue


			u2dt = u2curr + dth*vv
			u2dt = affine_transformation(u2dt)

			inliners = []
			ejs_temp = []
			e = 0

			ejs = symmetric_epipolar_distance(u1curr, u2dt, Fh)

			ejs = np.absolute(ejs)

			for index in xrange(len(ejs)):
				if ejs[index] < thr:
					inliners.append(index)
					ejs_temp.append(ejs[index])
					e = e + ejs[index]

			#writetofile(inliners, str(' inliners with threshold '), writefilename)
			#writetofile(len(inliners), str(' inliners length '), writefilename)
			#writetofile(e, str(' e '), writefilename)

			#found better candidate
			if len(inliners) > len(inliners_best) or (len(inliners) == len(inliners_best) and e < e_min):

				#writetofile(inliners, str('  better result appears  and new inliners  '), writefilename)
				#writetofile(len(inliners), str(' new inliners  length  '), writefilename)

				Ftres =Fh
				dtres = dth
				e_min = e
				inliners_best = inliners

				#writetofile(dtres, str(' new dtres '), writefilename)
				#writetofile(Ftres, str(' new Ftres '), writefilename)

				#Res = open(writefilename, 'a')
				#Res.write('\n end of the if   \n')
				#Res.close()
	if debug:
		Res = open(writefilename, 'a')
		Res.write('\n end of the for loop    \n')
		Res.close()
	return Ftres, dtres,  inliners_best, e_min





