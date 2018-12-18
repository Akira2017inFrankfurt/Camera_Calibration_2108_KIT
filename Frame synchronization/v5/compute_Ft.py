
import numpy as np
from generate_corresp import generate_corresp
from ransac_Ft_symmdis import ransac_Ft
#from ransac_Ft import ransac_Ft

# for test
from inandout import writetofile
# from inandout import errortest

def compute_Ft(tracks, num_tracks, fps1, fps2, offset1, offset2, thr, rounds_ransac, iter_rounds, k_max, k_min):
	writefilename = str('result_compute_Ft.txt')

	# before run function ransac_Ft, first clear the earlier data in txt
	Res = open('result_ransac_Ft.txt', 'w')
	Res.close()

	emin_Ft = np.inf
	Ftres = 0
	Ft_inliners = []
	inliners = 0

	# step is a array, dimension is bigger as iteration times, here is the iter_rounds
	step = np.zeros((50,1))
	step[0]= 2**k_min
	scale = k_min
	prev_inliners = 0
	skipped = 0
	r = 0
	dts =[]

	for i in range(iter_rounds):

		writetofile(i, str(' Iteration time '), writefilename)
		tracks1_corresp, tracks2_corresp = generate_corresp(tracks, num_tracks, fps1, fps2, offset1, offset2)

		# for test
		#errortest(tracks1_corresp,'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\u1.txt', float)
		#errortest(tracks2_corresp, 'C:\Users\hhl\Documents\GitHub\TwoViewUnsynch_original\TwoViewUnsynch-master\u2.txt', float)

		writetofile(offset2, str(' offset2 '), writefilename)
		#writetofile(tracks1_corresp, str(' tracks1_corresp'), writefilename)
		#writetofile(tracks2_corresp, str(' tracks2_corresp'), writefilename)

		Ftres1, dt1, inliners1, emin1_Ft = ransac_Ft(tracks1_corresp, tracks2_corresp, int(step[r]), thr, rounds_ransac)
		Ftres2, dt2, inliners2, emin2_Ft = ransac_Ft(tracks1_corresp, tracks2_corresp, int(-step[r]), thr, rounds_ransac)

		# input of the function 'ransac_Ft'

		#writetofile(step, str('step now is '), writefilename)
		writetofile(r, str('r of step[r]'), writefilename)

		# output of the function 'ransac_Ft'
		writetofile(Ftres1, str(' Ftres1'), writefilename)
		writetofile(len(inliners1), str(' len of inliners1'), writefilename)
		writetofile(dt1, str(' dt1'), writefilename)
		writetofile(Ftres2, str(' Ftres2 '), writefilename)
		writetofile(len(inliners2), str(' len of inliners2 '), writefilename)
		writetofile(dt2, str(' dt2'), writefilename)
		writetofile(emin1_Ft, str('emin1_Ft '), writefilename)
		writetofile(emin2_Ft, str('emin2_Ft '), writefilename)

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
			writetofile(step[r], str('step[r] change direction'), writefilename)

		writetofile(dt, str(' dt '), writefilename)
		dts.append(dt)
		Ft_inliners.append(inliners)

		if skipped > k_max:
			writetofile(skipped, str('skipped is appeard'), writefilename)
			writetofile(i, str(' Iteration end times is '), writefilename)
			break

		if prev_inliners >= len(inliners) and scale < k_max:
			scale = scale + 1
			step[r] = 2**scale
			skipped = skipped + 1
			writetofile(step[r], str('before is better, go to next round to try with a bigger step[r] \n may get better result, step[r]'), writefilename)
			continue

		if scale >= 0 and prev_inliners >= len(inliners):
			scale = 0
			step[r] = 2**scale
			skipped = skipped + 1
			writetofile(step[r], str('before is better and step[r]  can not increase\n so just go to next round '), writefilename)
			continue

		prev_inliners = len(inliners)
		step[r+1] = 2**scale

		writetofile(prev_inliners, str('no if is work, have new offset2 and prev_inliners is'), writefilename)
		writetofile(offset2, str(' offset2 before '), writefilename)

		offset2 = offset2 - (step[r] / fps2) * dts[r]

		writetofile(step[r], str(' step[r] '), writefilename)

		writetofile(offset2, str('  offset2 after '), writefilename)

		writetofile(dts[r], str(' dts[r] '), writefilename)

		skipped = 0
		writetofile(skipped, str('skipped set to zero again'), writefilename)
		r = r + 1
		writetofile(step.T, str('now the step have the value'), writefilename)

	writetofile(prev_inliners, str(' prev_inliners  '), writefilename)

	writetofile(step.T, str(' step '), writefilename)
	return Ftres, dts, offset2, Ft_inliners, emin_Ft, step


