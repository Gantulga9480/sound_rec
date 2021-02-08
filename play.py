import numpy as np
import sounddevice as sd
import tkinter as tk
from tkinter import filedialog
import csv

root = tk.Tk()
root.sound_name = filedialog.askopenfilename(initialdir="/home/lab-408/Desktop/github/",
                                             title="Select file",
                                             filetypes=(("npy file", "*.npy"),
                                                        ("all files", "*.*")))

fs = 12000
data = np.load(root.sound_name)
path = root.sound_name.split('/')
path.pop(-1)
path = [item + '/' for item in path]
path = ''.join(path) + 'label_time.csv'
label_list = []
with open(path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print(row)
        label_list.append(row)
len_ = len(label_list) // 2
for i in range(len_):
    s = (i+1)*2-2
    e = (i+1)*2-1
    start = int(label_list[s][1])
    end = int(label_list[e][1])
    print(label_list[s][0])
    sound = data[start:end]
    sd.play(sound, fs)
    sd.wait()
    print(label_list[e][0])
