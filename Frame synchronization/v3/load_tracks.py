import numpy as np
from compute_Ft import compute_Ft

filepath_1 = r'C:\Users\hhl\PycharmProjects\frame_syn\tracks_2.txt'
fps1 = 10.0
fps2 = 10.0
offset1 = 0.0
offset2 = 0.0
thr =0.001
rounds_ransac = 40
iter_rounds = 40
k_max = 3
k_min = 0
Result=open('result.txt', 'w')

def load_tracks(filepath):


    tracks =np.loadtxt(filepath, float)

    # number of image points in track 1
    n_tracks1 = int(tracks[0])
    tracks1 = tracks[1: 3*n_tracks1+1]

    n_tracks2 = int(tracks[3*n_tracks1+1])
    tracks2 = tracks[3*n_tracks1+2 : 3*(n_tracks2+n_tracks1)+2]

    tracks1 = np.reshape(tracks1, [n_tracks1,3])
    tracks2 = np.reshape(tracks2, [n_tracks2,3])

    Result.write('\n n_tracks1 is \n')
    s = str(n_tracks1)
    Result.write(s)

    Result.write('\n tracks1 is \n')
    s = str(tracks1)
    Result.write(s)

    Result.write('\n n_tracks2 is \n')
    s = str(n_tracks2)
    Result.write(s)

    Result.write('\n tracks2 is \n')
    s = str(tracks2)
    Result.write(s)


    return n_tracks1, tracks1, n_tracks2, tracks2

n1, t1, n2, t2 = load_tracks(filepath_1)
Ftres, dts, offset2, Ft_inliners, emin_Ft, step = compute_Ft(n1, t1, n2, t2, fps1, fps2, offset1, offset2, thr, rounds_ransac, iter_rounds, k_max, k_min)

Result.write('\n Ftres is \n')
s=str(Ftres)
Result.write(s)
Result.write('\n offset2 is \n')
s=str(offset2)
Result.write(s)
Result.close()






