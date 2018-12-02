
from generate_corresp import generate_corresp
from ransac_Ft import ransac_Ft
import numpy as np
from inandout import writetofile

def compute_Ft(n_tracks1, tracks1, n_tracks2,  tracks2, fps1, fps2, offset1, offset2, thr, rounds_ransac, iter_rounds, k_max, k_min):
    writefile = str('result_compute.txt')
    Res_compute = open('result_compute.txt', 'w')

    emin_Ft = np.inf
    Ftres = 0
    Ft_inliners = []
    inliners = 0

    step = []
    step.append(2 ** k_min)
    scale = k_min
    prev_inliners = 0
    skipped = 0
    r = 0
    dts =[]

    for i in range(iter_rounds):

        writetofile(i, str(' Iteration time '), str('result_compute.txt'))
        tracks1_corresp, tracks2_corresp = generate_corresp(n_tracks1, tracks1, n_tracks2, tracks2, fps1, fps2, offset1, offset2)

        writetofile(offset2, str(' offset2 '), str('result_compute.txt'))
        #writetofile(tracks1_corresp, str(' tracks1_corresp'), str('result_compute.txt'))
        #writetofile(tracks2_corresp, str(' tracks2_corresp'), str('result_compute.txt'))

        Ftres1, dt1, inliners1, emin1_Ft = ransac_Ft(tracks1_corresp, tracks2_corresp, step[r], thr, rounds_ransac)
        Ftres2, dt2, inliners2, emin2_Ft = ransac_Ft(tracks1_corresp, tracks2_corresp, -step[r], thr, rounds_ransac)

        # input of the function 'ransac_Ft'

        writetofile(step, str('step now is '), str('result_compute.txt'))
        writetofile(r, str('r of step[r]'), str('result_compute.txt'))

        # output of the function 'ransac_Ft'
        writetofile(Ftres1, str(' Ftres1'), str('result_compute.txt'))
        writetofile(len(inliners1), str(' len of inliners1'), str('result_compute.txt'))
        writetofile(dt1, str(' dt1'), str('result_compute.txt'))
        writetofile(Ftres2, str(' Ftres2 '), str('result_compute.txt'))
        writetofile(len(inliners2), str(' len of inliners2 '), str('result_compute.txt'))
        writetofile(dt2, str(' dt2'), str('result_compute.txt'))
        writetofile(emin1_Ft, str('emin1_Ft '), str('result_compute.txt'))
        writetofile(emin2_Ft, str('emin2_Ft '), str('result_compute.txt'))

        if len(inliners1) >= len(inliners2):
            dt = dt1
            Ftres = Ftres1
            inliners = inliners1
            step[r] = step[r]
        else:
            dt = dt2
            Ftres = Ftres2
            inliners = inliners2
            step[r] = -step[r]
            writetofile(step[r], str('step[r] change direction'), str('result_compute.txt'))

        writetofile(dt, str(' dt '), str('result_compute.txt'))
        dts.append(dt)
        Ft_inliners.append(inliners)

        if skipped > 30:
            writetofile(skipped, str('skipped is appeard'), str('result_compute.txt'))
            writetofile(i, str(' Iteration end times is '), str('result_compute.txt'))
            break

        if prev_inliners >= len(inliners) and scale < k_max:
            scale = scale + 1
            step[r] = 2**scale
            skipped = skipped + 1
            writetofile(step[r], str('before is better, go to next round to try with a bigger step[r] \n may get better result'), str('result_compute.txt'))
            continue

        if scale == k_max and prev_inliners >= len(inliners):
            scale = 0
            step[r] = 2**scale
            skipped = skipped + 1
            writetofile(step[r], str('before is better and step[r]  can not increase\n so just go to next round '), str('result_compute.txt'))
            continue

        prev_inliners = len(inliners)
        step.append(2**scale)

        writetofile(prev_inliners, str('no if is work, have new offset2 and prev_inliners is'), writefile)
        writetofile(offset2, str(' offset2 before '), str('result_compute.txt'))

        offset2 = offset2 - (step[r] / fps2) * dts[r]

        writetofile(step[len(step)-2], str(' step[r] '), str('result_compute.txt'))

        writetofile(offset2, str('  offset2 after '), str('result_compute.txt'))

        writetofile(dts, str(' dts '), str('result_compute.txt'))

        skipped = 0
        writetofile(skipped, str('skipped set to zero again'), writefile)
        r = r + 1
        writetofile(step, str('now the step have the value'), writefile)

    writetofile(prev_inliners, str(' prev_inliners  '), str('result_compute.txt'))

    writetofile(step, str(' step '), str('result_compute.txt'))
    return Ftres, dts, offset2, Ft_inliners, emin_Ft, step


