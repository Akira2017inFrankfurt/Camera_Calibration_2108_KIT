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

def tracks_List2Mat(tracks_List, n_tracks):
	temp = np.zeros((n_tracks, 3))
	count = 0
	row , col = temp.shape
	for i in xrange(row):
		for j in xrange(col):
			temp[i][j] = tracks_List[count]
			count += 1
	tracks_Mat= temp
	return tracks_Mat

def load_tracks(filepath_tracks):

	f = open(filepath_tracks, 'r')
	tracks=[]
	tracks_num=[]
	for line in f.readlines():
		curline =  line.strip().split(" ")
		floatline = map(float, curline)
		n_tracks = int(floatline[0])
		tracks_num.append(n_tracks)
		linetracks = floatline[1: 3 * n_tracks + 1]
		tracks.append(tracks_List2Mat(linetracks, n_tracks))

	return tracks, tracks_num

filepath_tracks = r'D:\Praktikum\literatur_Frame\20offset.txt'

rounds_test = 1
fps1 = 10.0
fps2 = 10.0
offset1 = 0.0
offset2 = 0.0
thr = 0.1
rounds_ransac = 50
rounds_iteration = 50
k_max = 6
k_min = 0

Res = open('result.txt', 'w')
Res.write('filepath_tracks is %s. \nthr is %s. \nrounds_ransac is %s. \n' % (filepath_tracks, thr, rounds_ransac))
Res.close()

source_tracks, source_num = load_tracks(filepath_tracks)

for i in xrange(rounds_test):

	Ftres, dts, offset2, Ft_inliners, emin_Ft, step = compute_Ft(source_tracks, source_num, fps1, fps2, offset1, offset2, thr, rounds_ransac, rounds_iteration, k_max, k_min, debug=False)

	Res = open('result.txt', 'a')

	Res.write('\n Ftres is \n')
	s = np.array2string(Ftres, formatter={'float_kind': lambda Ftres: "%.4f" % Ftres})
	Res.write(s)

	Res.write('\noffset2, %f, \n ' % offset2)
	Res.close()












