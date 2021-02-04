import numpy as np
import sounddevice as sd
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.sound_name = filedialog.askopenfilename(initialdir="/home/lab-408/Desktop/github/sound_rec/",
                                             title="Select file",
                                             filetypes=(("npy file", "*.npy"),
                                                        ("all files", "*.*")))

data = np.load(root.sound_name)
fs = 12000

sd.play(data, fs)
sd.wait()
