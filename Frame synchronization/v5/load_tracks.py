import numpy as np
from compute_Ft import compute_Ft

filepath_tracks = r'D:\Praktikum\literatur_Frame\Kitti_tracks_1.txt'
fps1 = 10.0
fps2 = 10.0
offset1 = 0.0
offset2 = 0.0
thr =2
rounds_ransac = 200
iter_rounds = 50
k_max = 6
k_min = 0
Result=open('result.txt', 'w')
Res = open('result_compute_Ft.txt', 'w')
Res.close()

def Trackslist2Mat(Matlist, n_tracks):
	temp_M = np.zeros((n_tracks, 3))
	count=0
	for i in range(temp_M.shape[0]):
		for j in range(temp_M.shape[1]):
			temp_M[i][j] = Matlist[count]
			count += 1
	Matlist = temp_M
	return Matlist

def load_tracks(filepath):

	f = open(filepath, 'r')
	tracks=[]
	tracks_num=[]
	for line in f.readlines():
		curline =  line.strip().split(" ")
		floatline = map(float, curline)
		n_tracks = int(floatline[0])
		tracks_num.append(n_tracks)
		linetracks = floatline[1: 3 * n_tracks + 1]
		tracks.append(Trackslist2Mat(linetracks, n_tracks))

	return tracks, tracks_num

source_tracks, source_num = load_tracks(filepath_tracks)
Ftres, dts, offset2, Ft_inliners, emin_Ft, step = compute_Ft(source_tracks, source_num, fps1, fps2, offset1, offset2, thr, rounds_ransac, iter_rounds, k_max, k_min)

Result.write('\n Ftres is \n')
s = str(Ftres)
Result.write(s)

Result.write('\n offset2 is \n')
s = str(offset2)
Result.write(s)

Result.close()






