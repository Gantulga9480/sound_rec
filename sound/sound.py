"""
Sound
=====

Created for ease of use in small projects using the sounddevice

git --> Gantulga9480.sound_rec
"""
import numpy as np
import sounddevice as sd
from queue import Queue, Full, Empty
from . utils import *
import sys

sys.dont_write_bytecode = True


class PathError(Exception):
    """Raises when no path is given"""
    pass


class SizeError(Exception):
    """ Riased when requested data size is bigger than actual data size """
    pass


class Sound:

    def __init__(self, device=None, channels=1, samplerate=None,
                 downsample=1, dtype=np.float32):
        self._device = device
        if samplerate is None:
            device_info = sd.query_devices(device, 'input')
            samplerate = device_info['default_samplerate']
        self._samplerate = samplerate
        self._channels = channels
        self._downsample = downsample
        self._dtype = dtype
        self._save_path = r'sound_cache/data'
        self._sound_buffer = Queue()
        self._max_buffer_size = 400_000

    def recorder(self):
        """
        Returns
        -------
        InputStream :
            Creates and returns InputStream object from current Sound class.
        """
        self._stream = sd.InputStream(device=self._device,
                                      channels=self._channels,
                                      samplerate=self._samplerate,
                                      callback=self.callback,
                                      dtype=self._dtype)
        return self._stream

    def player(self, data=None, fs=None, wait=False):
        """
        Playes back data from numpy.ndarray .

        Parameters
        ----------
            data : numpy.ndarray
                If data is not specified it playes current data in buffer.
            fs : int
                Sampling rate for playing sound data.
            wait : bool
                If True, the player blocks code execution until finished
                playing the current data.
        """
        fs = fs if fs else self._samplerate
        if data:
            sd.play(data, fs)
        else:
            data = self.get_data()
            sd.play(data, fs)
        if wait:
            sd.wait()
        else:
            pass

    def save(self, path=None, data=None):
        """
        Saves sound data from numpy.ndarray to *.npy file in given path.

        Parameters
        ----------
            path : str
                If specified, saves the current data to this path.
                If omitted, uses data caching path
            data : numpy.ndarray
                Data to be saved to the given path.
                If omitted, saves the current buffer data.
        """
        path = path if path else self._save_path + '.npy'
        data = data if data else self._sound_buffer
        np.save(path, data)

    def load(self, path):
        """
        Returns
        -------
        numpy.ndarray
            Loads numpy.npy data from given path.
            If path is not found, raises FileNotFoundError.
        """
        try:
            data = np.load(path)
        except FileNotFoundError:
            print(f"Can't load file from {path}")
        return data

    @logger
    def callback(self, indata, frames, times, status):
        """
        This is called for each audio block.
        If overwritten, indata must be saved to queue object in order to
        obtain sound input.
        """
        self._sound_buffer.put(indata[::self._downsample])

    @logger
    def get_data(self, size=None):
        """
        Returns numpy.ndarray form buffer.
        If size is not specified, sets size to its current buffer size.
        if size is bigger than current buffer size, raises SizeError.
        """
        data = np.zeros((1, self._channels), dtype=np.float32)
        q_size = self._sound_buffer.qsize()
        if size is None:
            size = q_size
        elif size > q_size:
            print("input size is bigger than current buffer size")
            raise SizeError
        for _ in range(size):
            try:
                tmp = self._sound_buffer.get_nowait()
                data = np.concatenate((data, tmp), axis=0)
            except Empty:
                break
        return data
