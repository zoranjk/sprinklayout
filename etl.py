import numpy as np

def csv_to_np(fileloc:str) -> np.ndarray:
    ''' Takes a CSV file and returns a 2D numpy array. '''
    return np.loadtxt(open(fileloc, "rb"), delimiter=",")