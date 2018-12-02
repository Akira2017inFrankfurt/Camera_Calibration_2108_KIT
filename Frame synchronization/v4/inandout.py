import numpy as np

def test(filepath):

    data = np.loadtxt(filepath, float)

    return data

def writetofile(result, name, txt_name):
    Res = open(txt_name , 'a')
    Res.write('\n')
    Res.write(name)
    Res.write(' is \n')
    s = str(result)
    Res.write(s)
    Res.write(' \n')
    Res.close()

def errortest(Pyresult, Matresultfilename, dtype):
    filepath = Matresultfilename
    c_matlab = test(filepath, dtype)
    c_matlab = np.reshape(c_matlab, Pyresult.shape)
    c_test = c_matlab - Pyresult

    check_m = []
    Res=open('error.txt', 'a')
    Res.write('\n check_m value   \n')
    for i in range(c_test.shape[0]):
        for j in range(c_test.shape[1]):
            if c_test[i][j] > 10 ** (-6):
                #check_m.append(i * c_test.shape[1] + j + 1)
                check_m.append(c_matlab[i][j])
                check_m.append(Pyresult[i][j])
                check_m.append([i, j])
    s = str(check_m)
    Res.write(s)
    Res.close()
