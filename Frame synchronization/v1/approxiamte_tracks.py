def approxiamte_tracks(time1, time2,  fps, offset, tracks2)
    tracks2_corresp = np.zeros(ntracks1*2).reshape(ntracks1, 2)
    for index_1 in range(len(time1)):
        # for index_2 in range(len(time2)):
        # index_1=0
        idxs = np.zeros(ntracks1)
        i = 0
        for index_2 in range(len(time2)):
            if time2[index_2] > time1[index_1]:
                idxs[i] = index_2
                i = i + 1
        #print idxs
        if idxs.max == 0:
            tracks2_corresp[index_1] = tracks2[len(tracks2) - 1][1:3]
        else:
            id = int(idxs[0])
            #print 'id值为', id
            if id == 0:
                tracks2_corresp[index_1] = tracks2[0][1:3]
            else:
                interp1 = tracks2[id - 1][1:3]
                interp2 = tracks2[id][1:3]
                #print interp1, interp2, '对应值'
                dt = (time1[index_1] - time2[id - 1]) / (time2[id] - time2[id - 1])
                #print 'dt 为', dt
                tracks2_corresp[index_1] = interp1 + dt * (interp2 - interp1)
    #print tracks2_corresp, tracks2_corresp.shape

    return tracks2_corresp