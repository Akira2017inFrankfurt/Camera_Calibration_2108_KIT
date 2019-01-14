#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 14 Jan 2019
@author: Hongliang (xmuhhl@outlook.com)
"""

import numpy as np

def test(filepath, dtype=float):

	data = np.loadtxt(filepath, dtype)

	return data

def writetofile(result, name, txt_name):
	Res = open(txt_name , 'a')
	Res.write('\n')
	Res.write(name)
	Res.write(' is \n')
	s = str(result)
	Res.write(s)
	Res.write(' \n')
	Res.close()

def errortest(Pyresult, Matresultfilename, dtype = float, ismatrix = True):
	filepath = Matresultfilename
	if ismatrix:
		c_matlab = test(filepath, dtype)
		c_matlab = np.reshape(c_matlab, Pyresult.shape)
		c_test = c_matlab - Pyresult
		check_m = []
		Res=open('error.txt', 'a')
		Res.write('\n')
		s=str(Matresultfilename)
		Res.write(s)
		Res.write('\n')
		for i in xrange(c_test.shape[0]):
			for j in xrange(c_test.shape[1]):
				if c_test[i][j] > 10 ** (-4):
					check_m.append(c_matlab[i][j])
					check_m.append(Pyresult[i][j])
					check_m.append(c_test[i][j])
					check_m.append([i, j])
		s = str(check_m)
		Res.write(s)
	else:
		c_matlab = test(filepath, dtype)
		c_matlab = np.reshape(c_matlab, Pyresult.shape)
		c_test = c_matlab - Pyresult
		check_m = []
		Res=open('error.txt', 'a')
		Res.write('\n check_m value   \n')
		for i in xrange(c_test.shape[0]):
			if c_test[i] > 10**(-6):
				check_m.append(c_matlab[i])
				check_m.append(Pyresult[i])
				check_m.append(c_test[i])
				check_m.append([i])
		s = str(check_m)
		Res.write(s)
	Res.close()
