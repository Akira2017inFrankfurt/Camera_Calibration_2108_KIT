#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 14 Jan 2019
@author: Hongliang (xmuhhl@outlook.com)
"""

import numpy as np

def frame2time(frame, fps, offset):
    return offset + (frame/fps)

def approxiamte_tracks(time1, time2,  tracks2, n_track1):
    tracks2_corresp = np.zeros(n_track1*2).reshape(n_track1, 2)
    for index_1 in xrange(len(time1)):
        idxs = np.zeros(len(time2))
        i = 0
        for index_2 in xrange(len(time2)):
            if time2[index_2] > time1[index_1]:
                idxs[i] = index_2
                i = i + 1

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

def generate_correspondence(tracks, num, fps1, fps2, offset1, offset2):
    pot_1 = 0
    for i in xrange(len(num)/2):
        pot_1 += num[i*2]

    tracks1_corresp = np.zeros((pot_1, 2))
    tracks2_corresp = np.zeros((pot_1, 2))
    inpos_tracks1 = 0

    for i in xrange(len(tracks)/2):

        add_num1 = num[i*2]

        time1 = np.zeros(add_num1)
        for index in xrange(tracks[i*2].shape[0]):
            time1[index] = frame2time(tracks[i*2][index][0], fps1, offset1)

        add_num2 = num[i*2+1]

        time2 = np.zeros(add_num2)
        for index in xrange(tracks[i*2+1].shape[0]):
            time2[index] = frame2time(tracks[i*2+1][index][0], fps2, offset2)

        tracks1_corresp[inpos_tracks1:inpos_tracks1 + add_num1, :] = tracks[i*2][:, 1:3]
        tracks2_corresp[inpos_tracks1:inpos_tracks1 + add_num1, :] = approxiamte_tracks(time1, time2, tracks[i*2+1], add_num1)

        inpos_tracks1 += add_num1

    return tracks1_corresp, tracks2_corresp



