import numpy as np
from scipy.linalg import null_space
from solver_F_unsynchron_a_sturmfels import solver_F_unsynchron_a_sturmfels

# for test
'''
from inandout import test
from inandout import errortest
filepath = r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\\xp.txt'
xp = test(filepath, float)
xp = np.reshape(xp,(8,3))
filepath = r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\\x.txt'
x = test(filepath, float)
x = np.reshape(x, (8,3))
filepath = r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\\v.txt'
v = test(filepath, float)
v = np.reshape(v, (8,2))
'''

def F_dt_8pt(xp, x, v):
	#xp is u1s, x is u2
	#input xp and x is 8*2 matrix

	M = np.array([ \
		v[:, 0] * xp[:, 0], x[:, 0] * xp[:, 0], v[:, 0] * xp[:, 1], x[:, 0] * xp[:, 1], \
		v[:, 0], x[:, 0], \
		v[:, 1] * xp[:, 0], x[:, 1] * xp[:, 0], v[:, 1] * xp[:, 1], x[:, 1] * xp[:, 1], \
		v[:, 1], x[:, 1], \
		xp[:, 0], xp[:, 1], \
		np.ones((1, x.shape[0])) \
		])

	temp_M = np.zeros((8, 15))
	for i in range(temp_M.shape[1]):
		temp_M[:, i] = M[i]
	M = temp_M

	M2 = np.array( [M[:, 1], M[:, 3], M[:, 5], M[:, 7], M[:, 9], M[:, 11], M[:, 12], M[:, 13], M[:, 14], M[:, 0], M[:, 2], M[:, 4], M[:, 6], M[:, 8], M[:, 10]])
	M2 = M2.T

	'''''
	Res = open('error.txt', 'w')
	Res.close()
	#errortest(M, r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\M.txt', float)
	errortest(M2, r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\M2.txt', float)
	'''
	n = null_space(M2)

	#errortest(n, r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\n.txt', float )

	temp_matrix = np.ones((n.shape[0] + 1, n.shape[1]))
	temp_matrix[1:n.shape[0] + 1, :] = n
	temp_n = temp_matrix

	a, b, c, d, e, f = solver_F_unsynchron_a_sturmfels(temp_n[:, 0], temp_n[:, 1], temp_n[:,2], temp_n[:,3], temp_n[:, 4], temp_n[:,5], temp_n[:,6])

	# use input from matlab to test
	''''
	filepath = r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\a.txt'
	xp = test(filepath, float)
	a = np.reshape(xp, (8,1))
	filepath = r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\b.txt'
	xp = test(filepath, float)
	b = np.reshape(xp, (8,1))
	filepath = r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\c.txt'
	xp = test(filepath, float)
	c = np.reshape(xp, (8,1))
	filepath = r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\d.txt'
	xp = test(filepath, float)
	d = np.reshape(xp, (8,1))
	filepath = r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\e.txt'
	xp = test(filepath, float)
	e = np.reshape(xp, (8,1))
	filepath = r'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\f.txt'
	xp = test(filepath, float)
	f = np.reshape(xp, (8,1))
	'''

	FF = np.zeros((15, 1))
	F = np.zeros((len(a), 9))
	u = np.zeros(len(a))
	for i in range(len(a)):
		FF = a[i]* n[:, 0] + b[i]* n[:, 1] + c[i]* n[:, 2] + d[i]* n[:, 3] + e[i]* n[:, 4] + f[i]*n[:, 5] + n[:, 6]
		F[i, :] = FF[0:9]
		u[i] = FF[9]/FF[0]
	return F, u

# for test
'''
F_test, u_test = F_dt_8pt(xp, x, v)
Fh = F_test[3]
Fh = np.reshape(Fh, (3,3)).T
print 'xx'
'''

