"""
    aaa
"""

from player import Player
from recorder import Recorder
from analysis import Analysis
from synthesizer import Synthesizer

import time
import numpy as np

from collections import deque

# import sys

class Ketter:
    _player = Player()

    # 正弦波をスピーカーから出力してみる
    # from generator import Generator
    # g = Generator()
    #
    # freqs = [500, 580, 640, 1200]
    # for f in freqs:
    #    print(f)
    #    p.speaker(g.sin(0.5, f, p.fs, 0.5))

    _analyze = Analysis(fs=_player.fs, frame_period=_player.fs / 2000)
    _synthe = Synthesizer(fs=_player.fs, frame_period=_analyze.period)
    _chunk_size = int(_player.fs * _analyze.period / 1000)
    _recorder = Recorder(fs=_player.fs)

    _processing_length = _recorder.frames_per_buffer // _chunk_size
    _processing_block_count = 1
    _buffer_count = _processing_length * 8
    _data = deque(maxlen=_buffer_count * _chunk_size * _processing_block_count)
    _data.extend(np.zeros(_chunk_size * _buffer_count))

    _f0_converter = lambda self, x: x
    _mc_converter = lambda self, x: x

    def setF0Converter(self, callback):
        self._f0_converter = callback
    
    def setMelcepstrumConverter(self, callback):
        self._mc_converter = callback

    def start(self):
        self._recorder.start()
        print("start")
        try:
            synthe_start_frame = 1
            synthe_end_frame = self._processing_length * self._processing_block_count + synthe_start_frame

            count = 0
            while True:
                time.sleep(0.002)
                x, empty = self._recorder.read()
                if not empty:
                    x = np.array(x)
                    self._data.extend(x)
                    count = count + 1

                if count >= self._processing_block_count:
                    count = 0
                    # start_time = time.time()
                    f0, _, ap, mc = self._analyze.analyze(np.array(self._data))
                    f0 = f0[synthe_start_frame:synthe_end_frame]
                    # sp = sp[synthe_start_frame:synthe_end_frame]
                    ap = ap[synthe_start_frame:synthe_end_frame]
                    mc = mc[synthe_start_frame:synthe_end_frame]
                    # analyze_time = time.time() - start_time

                    f0 = self._f0_converter(f0)
                    mc = self._mc_converter(mc)
                    # convert_time = time.time() - analyze_time - start_time

                    converted = self._synthe.synthesize(f0, None, ap, mcep = mc)
                    # finish_time = time.time() - convert_time - start_time
                    # sys.stdout.write("\r %f: %f: %f: %f" % (1., analyze_time,
                    #                                         convert_time, finish_time))
                    self._player.speaker(converted)

        except KeyboardInterrupt:
            self._recorder.terminate()
            self._player.close()

        print("finish")
