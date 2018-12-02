import numpy as np

def test(filepath):

    data = np.loadtxt(filepath, float)

    return data