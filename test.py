import numpy as np
import time
import sound

sd = sound.Sound(device=1,
                 channels=2)

stream = sd.recorder()
with stream:
    for i in range(100):
        time.sleep(0.1)
sd.player(wait=True)
