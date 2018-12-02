#def load_tracks_numpy(todo)
#todo decide which input_parameter is better  ''absfilepath"  oder "filename"
import numpy as np
tracks =np.loadtxt("C:\\Users\\hhl\\PycharmProjects\\Frame_synchronsization\\tracks_test.txt", float)
    #tracks =np.loadtxt("todo", float)
ntracks1=tracks[0]
ntracks1 = int(ntracks1)
tracks1=tracks[1: 3*ntracks1+1]
ntracks2 = tracks[3*ntracks1+1]
ntracks2 = int(ntracks2)
tracks2=tracks[3*ntracks1+2 : 3*(ntracks2+ntracks1)+2]
tracks1 =np.reshape(tracks1, [ntracks1,3])
tracks2 =np.reshape(tracks2, [ntracks2,3])
    #return tracks1, tracks2




