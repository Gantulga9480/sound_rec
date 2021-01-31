import numpy as np
import sounddevice as sd
import time
from parameter import *
from paho_mqtt import PahoMqtt as Host


def audio_callback(indata, frames, times, status):
    """This is called (from a separate thread) for each audio block."""
    data = indata[::DOWNSAMPLE]
    mic.buffer = np.concatenate((mic.buffer, data), axis=0)
    if mic.buffer.shape[0] > SOUND_BUFFER_MAX_CAPACITY:
        mic.buffer = np.delete(mic.buffer, 0, axis=0)
        mic.buffer_index += mic.buffer.shape[0]
        np.save(f'sound_cache/data_{mic.file_index}.npy', mic.buffer)
        mic.buffer = np.zeros((1, CHANNEL), dtype=np.float32)
        mic.file_index += 1


mic = Host(BROKER, 'mic_1')
mic.loop_start()

stream = sd.InputStream(device=DEVICE, channels=CHANNEL,
                        samplerate=SAMPLERATE, callback=audio_callback,
                        dtype=np.float32)

while mic.run:
    if mic.is_streaming:
        print(f'{mic.info} record start')
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
