
from generate_corresp import generate_corresp
from ransac_Ft import ransac_Ft

def compute_Ft(n_tracks1, tracks1, n_tracks2,  tracks2, fps1, fps2, offset1, offset2, thr, rounds_ransac, iter_rounds, k_max, k_min):

    Res_compute = open('result_compute.txt', 'w')

    emin_Ft = []
    Ftres = []
    Ft_inliners = []
    inliners =[]

    step = []
    step.append(2 ** k_min)
    scale = k_min
    prev_inliners = 0
    skipped = 0
    r = 0
    dts =[]

    for i in range(iter_rounds):

        Res_compute.write('\n offset2 is  \n')
        s = str(offset2)
        Res_compute.write(s)

        tracks1_corresp, tracks2_corresp = generate_corresp(n_tracks1, tracks1, n_tracks2, tracks2, fps1, fps2, offset1, offset2)

        Res_compute.write('\n tracks1_corresp  \n')
        s = str(tracks1_corresp)
        Res_compute.write(s)

        Res_compute.write('\n tracks2_corresp  \n')
        s = str(tracks2_corresp)
        Res_compute.write(s)

        Ftres1, dt1, inliners1, emin_Ft = ransac_Ft(tracks1_corresp, tracks2_corresp, step[r], thr, rounds_ransac)
        Ftres2, dt2, inliners2, emin_Ft = ransac_Ft(tracks1_corresp, tracks2_corresp, -step[r], thr, rounds_ransac)

        Res_compute.write('\n Ftres1  \n')
        s = str(Ftres1)
        Res_compute.write(s)

        Res_compute.write('\n inliners1  \n')
        s = str(inliners1)
        Res_compute.write(s)

        Res_compute.write('\n Ftres2  \n')
        s = str(Ftres2)
        Res_compute.write(s)

        Res_compute.write('\n inliners2  \n')
        s = str(inliners2)
        Res_compute.write(s)

        Res_compute.write('\n emin_Ft   \n')
        s = str(emin_Ft)
        Res_compute.write(s)

        if len(inliners1) > len(inliners2):
            dt = dt1
            Ftres = Ftres1
            inliners = inliners1
            step[r] = step[r]
        else:
            dt = dt2
            Ftres = Ftres2
            inliners = inliners2
            step[r] = -step[r]

        Res_compute.write('\n dt  \n')
        s = str(dt)
        Res_compute.write(s)

        dts.append(dt)
        Ft_inliners.append(inliners)

        if skipped > k_max:
            Res_compute.write('\n skipped is appeard  \n')
            s = str(skipped)
            Res_compute.write(s)
            break


        if prev_inliners >= len(inliners) and scale < k_max :
            scale = scale + 1
            step[r] = 2**scale
            skipped = skipped + 1
            Res_compute.write('\n before is better and stop this round , direkt go to next round  \n and step[r] can increase \n')
            s = str(step[r])
            Res_compute.write(s)
            continue

        if scale == k_max and prev_inliners >= len(inliners):
            scale = 0
            step[r] = 2**scale
            skipped = skipped + 1
            Res_compute.write('\n before is better and stop this round \n and step[r]  can not increase is \n')
            s = str(step[r])
            Res_compute.write(s)
            continue

        prev_inliners = len(inliners)
        step.append(2**scale)

        Res_compute.write('\n offset2 before  \n')
        s = str(offset2)
        Res_compute.write(s)

        offset2 = offset2 - (step[len(step) - 2] / fps2) * dts[r]

        Res_compute.write('\n step[len(step)-2]  \n')
        s = str(step[len(step)-2])
        Res_compute.write(s)

        Res_compute.write('\n offset2 after  \n')
        s = str(offset2)
        Res_compute.write(s)

        Res_compute.write('\n dts is  \n')
        s = str(dts)
        Res_compute.write(s)


        skipped = 0
        r = r + 1

    Res_compute.write('\n prev_inliners is  \n')
    s = str(prev_inliners)
    Res_compute.write(s)

    Res_compute.write('\n step  \n')
    s = str(step)
    Res_compute.write(s)
    Res_compute.close()
    return Ftres, dts, offset2, Ft_inliners, emin_Ft, step


