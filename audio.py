import numpy as np
import sounddevice as sd
import time
from matplotlib import pyplot as plt

channel = 1
device = 7
samplerate = 48000
data = np.zeros((1,1), dtype=np.float32)
data_index = 0

max_val = 0.3

def audio_callback(indata, frames, times, status):
    """This is called (from a separate thread) for each audio block."""
    global data, data_index
    if status:
        print(status)
    data_1 = indata[::4]
    print(indata.shape)
    data = np.concatenate((data, data_1), axis=0)
    if data.shape[0] > 500000:
        np.save(f'data_{data_index}.npy', data)
        data_index += 1
        data = np.zeros((1,1), dtype=np.float32)


stream = sd.InputStream(device=device, channels=channel,
                        samplerate=samplerate, callback=audio_callback,
                        dtype=np.float32)
with stream:
    i = 0
    print('record start')
    while i < 100:
        i += 1
        time.sleep(0.1)
    print('record end')

np.save('data.npy', data)
