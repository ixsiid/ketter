import struct
import pyaudio
import queue

import sys


class Recorder:
    def __init__(self, fs=16000, frames_per_buffer=1024):
        self._que = queue.Queue(maxsize=1024)
        
        _port = pyaudio.PyAudio()
        self._stream = _port.open(
            format=pyaudio.paFloat32, channels=1, rate=fs,
            input=True, output=False, frames_per_buffer=frames_per_buffer,
            stream_callback=self._input_callback, start=False)
        self.frames_per_buffer = frames_per_buffer

    def _input_callback(self, in_data, frame_count, time_info, status_flags):
        fmt = 'f' * frame_count
        x = struct.unpack(fmt, in_data)
        self._que.put(x)
        return (None, pyaudio.paContinue)

    def start(self):
        self._stream.start_stream()

    def terminate(self):
        self._stream.stop_stream()
        self._stream.close()

    def read(self):
        data = []
        empty = True
        if not self._que.empty():
            data = self._que.get()
            empty = False

        return data, empty
