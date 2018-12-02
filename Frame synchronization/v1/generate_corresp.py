def generate_corresp(ntracks1, ntracks2, tracks1, tracks2, fps1, fps2, offset1, offset2)
    import numpy as np
    import frame2time
    import approxiamte_tracks
    time1 = np.zeros(ntracks1)
    for index in range(tracks1.shape[0]):
        time1[index] = frame2time(tracks1[index][0], fps1, offset1)
        #print time1[index]
    time2 = np.zeros(ntracks2)
    for index in range(tracks2.shape[0]):
        time2[index] = frame2time(tracks2[index][0], fps2, offset2)
        # print time2[index]
    tracks1_corresp = np.zeros(ntracks1 * 2).reshape(ntracks1, 2)
    tracks1_corresp = tracks1[:, 1:3]
    tracks2_corresp = approximate_tracks(time1, time2,  fps2, offset2, tracks2)
    return tracks1 _corresp, tracks2_corresp



