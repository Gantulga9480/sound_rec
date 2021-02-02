import numpy as np
from numpy.lib.format import BUFFER_SIZE
import paho.mqtt.client as mqtt
from parameter import *
import sounddevice as sd
import os


class PahoMqtt:

    def __init__(self, broker, info, port=1883,
                 raw_msg=False):

        self.__broker = broker
        self.__port = port
        self.info = info
        self.__client = mqtt.Client(f"{info} control")
        if not raw_msg:
            self.__client.on_message = self.__on_message
        else:
            self.__client.on_message = self.__on_message_raw
        self.__client.on_connect = self.__on_connect
        self.__client.on_publish = self.__on_publish
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.wait_for_publish = self.__wait_for_publish
        self.__client.connect(self.__broker, self.__port)

        self.is_streaming = False
        self.is_idle = True
        self.is_playing = False
        self.label = list()
        self.path = None
        self.run = True
        self.file_index = 0
        self.buffer_index = 0
        self.buffer = np.zeros((1, CHANNEL), dtype=np.float32)
        self.data = np.zeros((1, CHANNEL), dtype=np.float32)

    def __on_connect(self, client, userdata, level, buf):
        self.reset()
        self.publish(topic='sound', msg=f'{self.info}, connected')
        self.subscribe(topic='sound', qos=0)
        print(f"{self.info} connected")

    def __on_message(self, client, userdata, message):
        msg = message.payload.decode("utf-8", "ignore")
        msgs = msg.split("-")
        if msgs[0] == START:
            self.is_streaming = True
            self.is_playing = False
            self.is_idle = False
            self.path = msgs[1]
        elif msgs[0] == STOP:
            self.is_streaming = False
            self.is_playing = False
            self.is_idle = True
        elif msgs[0] == ACTIVITIE_START:
            lbl = self.buffer_index + self.buffer.shape[0]
            self.label.append([f'{msgs[1]} start', lbl])
        elif msgs[0] == ACTIVITIE_STOP:
            lbl = self.buffer_index + self.buffer.shape[0]
            self.label.append([f'{msgs[1]} end', lbl])
        elif msgs[0] == SAVE:
            self.save()
            self.reset()
        elif msgs[0] == RESET:
            self.reset()
        elif msgs[0] == PLAY:
            self.is_streaming = False
            self.is_playing = True
            self.is_idle = False

    def reset(self):
        self.is_streaming = False
        self.is_playing = False
        self.is_idle = True
        self.buffer = np.zeros((1, CHANNEL), dtype=np.float32)
        self.data = np.zeros((1, CHANNEL), dtype=np.float32)
        self.label.clear()
        self.buffer_index = 0
        self.file_index = 0
        i =  0
        while True:
            try:
                os.remove(f'sound_cache/data_{i}.npy')
            except FileNotFoundError:
                break
            i += 1
        print('[INFO] RESET ...')

    def save(self):
        print('[INFO] SAVING DATA ...')
        self.is_streaming = False
        self.is_playing = False
        self.is_idle = True
        i = 0
        self.data = np.zeros((1, CHANNEL), dtype=np.float32)
        while True:
            try:
                tmp = np.load(f'sound_cache/data_{i}.npy')
                self.data = np.concatenate((self.data, tmp), axis=0)
                os.remove(f'sound_cache/data_{i}.npy')
                i += 1
            except FileNotFoundError:
                break
        ss = self.path.split('/')
        os.makedirs(self.path)
        np.save(f'{self.path}/sound_{self.info}.npy', self.data)
        
        label_file = open(f'{self.path}/label_time.txt', '+w')
        with label_file:
            for item in self.label:
                label_file.write(f'{item[0]}, {item[1]}\n')
        print('[INFO] DONE SAVING DATA ...')

    def __on_message_raw(self, client, userdata, message):
        pass

    def __on_publish(self, client, userdata, result):
        print('[INFO] status published')

    def __on_disconnect(self, client, userdata, rc):
        print(f"[INFO] {self.info} disconnected")

    def __wait_for_publish(self):
        print('[INFO] waiting to publish status')

    def disconnect(self):
        self.__client.disconnect()

    def publish(self, topic, msg, qos=0):
        self.__client.publish(topic, payload=msg, qos=qos)

    def subscribe(self, topic, qos=0):
        self.__client.subscribe(topic, qos=qos)

    def loop_start(self):
        self.__client.loop_start()

    def callback(self, indata, frames, times, status):
        """This is called (from a separate thread) for each audio block."""
        data = indata[::DOWNSAMPLE]
        self.buffer = np.concatenate((self.buffer, data), axis=0)
        if  self.buffer.shape[0] > SOUND_BUFFER_MAX_CAPACITY:
            self.buffer = np.delete(self.buffer, 0, axis=0)
            self.buffer_index += self.buffer.shape[0]
            np.save(f'sound_cache/data_{self.file_index}.npy', self.buffer)
            self.buffer = np.zeros((1, CHANNEL), dtype=np.float32)
            self.file_index += 1

    def create_streamer(self):
        streamer = sd.InputStream(device=DEVICE, channels=CHANNEL,
                                  samplerate=SAMPLERATE, callback=self.callback,
                                  dtype=np.float32)
        return streamer
