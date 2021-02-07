from scipy.io.wavfile import write
import numpy as np
samplerate = 48000
data = np.load('data/2021_02_08/01_09_59/sound_mic_1.npy')
write('data.wav', samplerate, data)
