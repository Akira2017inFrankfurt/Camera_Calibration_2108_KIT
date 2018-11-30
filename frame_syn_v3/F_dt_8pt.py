import numpy as np
from scipy.linalg import null_space
from solver_F_unsynchron_a_sturmfels import solver_F_unsynchron_a_sturmfels


def F_dt_8pt(xp,x,v):
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

    n = null_space(M2)
    temp_matrix = np.ones((n.shape[0] + 1, n.shape[1]))
    temp_matrix[1:n.shape[0] + 1, :] = n
    temp_n = temp_matrix

    a, b, c, d, e, f = solver_F_unsynchron_a_sturmfels(temp_n[:, 0], temp_n[:, 1], temp_n[:,2], temp_n[:,3], temp_n[:, 4], temp_n[:,5], temp_n[:,6])
    FF = np.zeros((15, 1))
    F = np.zeros((len(a), 9))
    u = np.zeros(len(a))
    for i in range(len(a)):
        FF= a[i]* n[:,0] + b[i]* n[:,1] + c[i]* n[:,2] + d[i]* n[:,3] + e[i]* n[:,4] + f[i]*n[:,5] + n[:,6]
        F[i, :] = FF[0:9]
        u[i] = FF[9]/FF[0]
    return F, u

