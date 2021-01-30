import numpy as np
import sounddevice as sd
import time
import os


channel = 7
device = 7
samplerate = 48000
downsample = 1
index = 0
buffer = np.zeros((1, channel), dtype=np.float32)


def audio_callback(indata, frames, times, status):
    """This is called (from a separate thread) for each audio block."""
    global buffer, index
    print(indata.shape)
    data = indata[::downsample]
    buffer = np.concatenate((buffer, data), axis=0)
    if buffer.shape[0] > 300000:
        buffer = np.delete(buffer, 0, axis=0)
        np.save(f'data_{index}.npy', buffer)
        buffer = np.zeros((1, channel), dtype=np.float32)
        index += 1


stream = sd.InputStream(device=device, channels=channel,
                        samplerate=samplerate, callback=audio_callback,
                        dtype=np.float32)
with stream:
    i = 0
    print('record start')
    while i < 6000:
        i += 1
        time.sleep(0.1)
print('record end')
np.save(f'data_{index}.npy', buffer)
index = 0
datas = list()
while 1:
    try:
        datas.append(np.load(f'data_{index}.npy'))
        os.remove(f'data_{index}.npy')
        index += 1
    except FileNotFoundError:
        break

data = np.zeros((1, channel), dtype=np.float32)
print(len(datas))
for d in datas:
    data = np.concatenate((data, d), axis=0)
sd.play(data, samplerate/downsample)
sd.wait()
np.save('data.npy', data)
