import numpy as np
import sounddevice as sd
import time
from parameter import *
from paho_mqtt import PahoMqtt as Host


mic = Host(BROKER, NODE)
mic.loop_start()

while mic.run:
    if mic.is_streaming:
        print(f'{mic.info} record start')
        stream = mic.create_streamer()
        with stream:
            while mic.is_streaming:
                time.sleep(1)
                print(f'[INFO] {mic.info} is recording : {mic.buffer.shape[0]}')
        np.save(f'sound_cache/data_{mic.file_index}.npy', mic.buffer)
        print(f'{mic.info} record end')
    elif mic.is_idle:
        while mic.is_idle:
            print(f'[INFO] {mic.info} is in Idle')
            time.sleep(0.1)
    elif mic.is_playing:
        print(f'[INFO] {mic.info} is playing')
        sd.play(mic.data, SAMPLERATE/DOWNSAMPLE)
        sd.wait()
        mic.is_streaming = False
        mic.is_playing = False
        mic.is_idle = True
