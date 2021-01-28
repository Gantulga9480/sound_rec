import numpy as np
import sounddevice as sd
from matplotlib import pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--index', type=int)

args = parser.parse_args()

data_ind = args.index

data = np.load(f'data_{data_ind}.npy')
data = data*10
fs = 12000

a = data.shape


sd.play(data[:,0], fs)
sd.wait()
