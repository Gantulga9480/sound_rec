from scipy.io.wavfile import write
import numpy as np
samplerate = 12000
data = np.load('data/2021_02_08/02_57_30/sound_mic_1.npy')
write('data.wav', samplerate, data)
