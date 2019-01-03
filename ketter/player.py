import numpy as np
import struct
import pyaudio
import concurrent.futures


# 小分けでストリームに書き込んでみたけどあまりいみなさそう
# def _write_stream(stream, data):
    # chunk = 1024
    # sp = 0
    # buffer = data[sp:sp + chunk]
    # while buffer != b'':
    #     stream.write(buffer)
    #     sp = sp + chunk
    #     buffer = data[sp:sp + chunk]


class Player:
    fs = 16000
    _port = pyaudio.PyAudio()
    _stream = _port.open(
        format=pyaudio.paFloat32, channels=1, rate=fs, output=True)

    _executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    #再生用関数
    def speaker(self, data):
        # port.open が format=pyaudio.paInt16 の場合
        # data = [int(x * 32767.0) for x in data]# [-32768, 32767]の整数値に変換
        # data = struct.pack("f" * len(data), *data) # バイナリデータに変換

        # port.open が format=pyaudio.paFloat32 の場合
        data = struct.pack("f" * len(data), *data)

        # self._executor.submit(_write_stream, self._stream, data)
        self._executor.submit(self._stream.write, data)

    def close(self):
        self._executor.shutdown()
        self._stream.close()
