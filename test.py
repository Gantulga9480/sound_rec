import numpy as np
import time
import sound
from queue import Queue

def callback_1(indata, frames, times, status):
    print('data')
    buffer.put(indata)


buffer = Queue()
sd = sound.Sound(device=0,
           channels=1,
           samplerate=44100,
           downsample=1,
           callback=callback_1)


stream = sd.recorder()
with stream:
    for i in range(100):
        time.sleep(0.1)
data = sd.get_data(buffer)
sd.player(data, wait=True)
