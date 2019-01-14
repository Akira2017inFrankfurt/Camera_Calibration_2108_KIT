#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 14 Jan 2019
@author: Hongliang (xmuhhl@outlook.com)
"""

import numpy as np
from compute_Ft import compute_Ft

'''
Res = open('result_compute_Ft.txt', 'w')
Res.close()
'''

def Trackslist2Mat(Matlist, n_tracks):
	temp_M = np.zeros((n_tracks, 3))
	count=0
	for i in xrange(temp_M.shape[0]):
		for j in xrange(temp_M.shape[1]):
			temp_M[i][j] = Matlist[count]
			count += 1
	Matlist = temp_M
	return Matlist

def load_tracks(filepath):

	f = open(filepath, 'r')
	tracks=[]
	tracks_num=[]
	for line in f.readlines():
		curline =  line.strip().split(" ")
		floatline = map(float, curline)
		n_tracks = int(floatline[0])
		tracks_num.append(n_tracks)
		linetracks = floatline[1: 3 * n_tracks + 1]
		tracks.append(Trackslist2Mat(linetracks, n_tracks))

	return tracks, tracks_num

filepath_tracks = r'D:\Praktikum\literatur_Frame\-20offset.txt'

test_num = 1
fps1 = 10.0
fps2 = 10.0
offset1 = 0.0
offset2 = 0.0
thr = 0.1
rounds_ransac = 50
iter_rounds = 50
k_max = 6
k_min = 0

Res = open('result.txt', 'w')

s = str(filepath_tracks)
Res.write(s)
Res.write('\n')

Res.write('thr ')
s = str(thr)
Res.write(s)
Res.write('\n')

Res.write('rounds_ransac ')
s = str(rounds_ransac)
Res.write(s)
Res.write('\n')

Res.write('offset2')
Res.write('\n')

Res.close()

source_tracks, source_num = load_tracks(filepath_tracks)

for i in xrange(test_num):

	Ftres, dts, offset2, Ft_inliners, emin_Ft, step = compute_Ft(source_tracks, source_num, fps1, fps2, offset1, offset2, thr, rounds_ransac, iter_rounds, k_max, k_min, debug=False)

	Res = open('result.txt', 'a')

	'''
	Res.write('\n Ftres is \n')
	s = str(Ftres)
	Res.write(s)
	'''

	s = str(float(offset2))
	Res.write(s)
	Res.write(', ')
	Res.write('\n')

	Res.close()












