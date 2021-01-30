import numpy as np
import glob
import sounddevice as sd

index = 0
datas = list()
while 1:
    try:
        datas.append(np.load(f'data_{index}.npy'))
        index += 1
    except FileNotFoundError:
        break

data = np.zeros((1, 1), dtype=np.float32)
print(len(datas))
for d in datas:
    # print(d.shape)
    array = np.delete(d, 0, axis=0)
    # print(array.shape)
    data = np.concatenate((data, array), axis=0)

# print(data)

# data = data*10
fs = 44100
sd.play(data, fs)
sd.wait()
