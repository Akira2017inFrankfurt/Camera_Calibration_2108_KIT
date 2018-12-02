# 迭代计算函数

import ransac

# supposed a big number
N = 1000;

beta = [N]
inliers = [N]
T = [N]


def compute_Ft(list_0, list_1, k_max, p_max, p_min):
    beta[0] = 0
    # todo: the value of J
    i = j = 0
    skipped = 0
    d = pow(p_min, 2)
    inliers[0] = 0
    p = p_min
    k = 1

    while k < k_max:
        # todo refine the ransac function
        T[1], beta[1], inliers[1] = ransac(list_0[i], list_1[j], d)
        T[2], beta[2], inliers[2] = ransac(list_0[i], list_1[j], 0 - d)

        if inliers[1] > inliers[2]:
            inliers[k] = inliers[1]
            beta[k] = beta[1]
            T[k] = T[1]
        else:
            inliers[k] = inliers[2]
            beta[k] = beta[2]
            T[k] = T[2]

        if skipped > p_max:
            return T[k - 1], beta[k-1] + j + i
        elif inliers[k] < inliers[k-1]:
            if p < p_max:
                p += 1
            else:
                p = 0
            d = pow(p, 2)
            skipped += 1
        else:
            j += beta[k]
            skipped = 0
            k += 1