def ransac_Ft(u1, u2, interp_dist, thr, rounds, error_function)
    import numpy as np
    import random
    import F_dt_8pt
    inliners_best =
    emin = np.inf
    Ftres =
    dtres =
    nsamples =8
    # interp_dist =2
    if interp_dist > 0:
        start = 0
        finish = u1.shape[0] - interp_dist
        u2next = u2[interp_dist: u2.shape[0], :]
        # print u2.shape[0]
        # print u2[0:4]
        u2curr = u2[0: u2.shape[0] - interp_dist, :]
        u1curr = u1[0: u1.shape[0] - interp_dist, :]
    else:
        start = - interp_dist
        finish = u1.shape[0]
        u2curr = u2[-interp_dist: u2.shape[0],: ]
        u2next = u2[0: interp_dist + u2.shape[0],: ]
        u1curr = u1[-interp_dist: u1.shape[0], :]
    vv=u2next-u2curr
    for i in range(rounds):
        sample =random.sample(range(finish-start),nsamples)
        for i in range(nsamples):
            sample[i] = sample[i] + start
        u1s = u1[sample, :]
        u2s = u2[sample, :]
        sample_next = range(8)
        # print 'initial sample_next', sample_next
        for i in range(nsamples):
            sample_next[i] = sample[i] + interp_dist
        v=u2[sample_next,:]-u2[sample,:]
        F, dt, fun_contin = F_dt_8pt(u1s,u2s,v)
        #todo 解决这个for循环中断的方法，可以增加一个
        #F_dt_8pt的输出来解决
        if fun_contin
            continue

        #evaluate hypotheses


