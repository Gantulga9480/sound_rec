import numpy as np
import sounddevice as sd


data = np.load(f'data/2021_01_31/23_36_01/sound_mic_1.npy')
# data = data*10
fs = 12000

a = data.shape


sd.play(data, fs)
sd.wait()
