import numpy as np


def frame2time(frame, fps, offset):
    return offset + (frame/fps)


def approxiamte_tracks(time1, time2,  tracks2, n_track1):
    tracks2_corresp = np.zeros(n_track1*2).reshape(n_track1, 2)
    for index_1 in range(len(time1)):
        idxs = np.zeros(n_track1)
        i = 0
        for index_2 in range(len(time2)):
            if time2[index_2] > time1[index_1]:
                idxs[i] = index_2
                i = i + 1
        # print np.max(idxs)

        if np.max(idxs) == 0.0:
            tracks2_corresp[index_1] = tracks2[len(tracks2) - 1][1:3]
        else:
            id = int(idxs[0])

            if id == 0:
                tracks2_corresp[index_1] = tracks2[0][1:3]
            else:
                interp1 = tracks2[id - 1][1:3]
                interp2 = tracks2[id][1:3]

                dt = (time1[index_1] - time2[id - 1]) / (time2[id] - time2[id - 1])
                tracks2_corresp[index_1] = interp1 + dt * (interp2 - interp1)
    return tracks2_corresp


def generate_corresp(n_track1, tracks1, n_track2, tracks2, fps1, fps2, offset1, offset2):
    time1 = np.zeros(n_track1)
    for index in range(tracks1.shape[0]):
        time1[index] = frame2time(tracks1[index][0], fps1, offset1)

    time2 = np.zeros(n_track2)
    for ind in range(tracks2.shape[0]):
        time2[ind] = frame2time(tracks2[ind][0], fps2, offset2)

    tracks1_corresp = np.zeros(n_track1 * 2).reshape(n_track1, 2)
    tracks1_corresp = tracks1[:, 1:3]
    tracks2_corresp = approxiamte_tracks(time1, time2, tracks2, n_track1)
    return tracks1_corresp, tracks2_corresp



