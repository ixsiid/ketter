"""
    aaa
"""

from .player import Player
from .recorder import Recorder
from .analysis import Analysis
from .synthesizer import Synthesizer
from .synthesizer_spectrum import SynthesizerSpectrum
from .synthesizer_melcepstrum import SynthesizerMelcepstrum
from .synthesizer_diffvc import SynthesizerDiffVC

import time
import numpy as np

from collections import deque
import itertools

# import sys

class Ketter:
    def __init__(self, synthe='Melcepstrum'):
        self._player = Player()

        # 正弦波をスピーカーから出力してみる
        # from generator import Generator
        # g = Generator()
        #
        # freqs = [500, 580, 640, 1200]
        # for f in freqs:
        #    print(f)
        #    p.speaker(g.sin(0.5, f, p.fs, 0.5))

        self._analyze = Analysis(fs=self._player.fs, frame_period=self._player.fs / 2000)
        self._synthe = Synthesizer(fs=self._player.fs, frame_period=self._analyze.period)
        if synthe == "Melcepstrum":
            self._synthe = SynthesizerMelcepstrum(fs=self._player.fs, frame_period=self._analyze.period)
        if synthe == "Spectrum":
            self._synthe = SynthesizerSpectrum(fs=self._player.fs, frame_period=self._analyze.period)
        if synthe == "DiffVC":
            self._synthe = SynthesizerDiffVC(fs=self._player.fs, frame_period=self._analyze.period)

        _chunk_size = int(self._player.fs * self._analyze.period / 1000)
        self._recorder = Recorder(fs=self._player.fs)

        self._processing_length = self._recorder.frames_per_buffer // _chunk_size
        self._processing_block_count = 1
        _buffer_count = self._processing_length * 8
        self._data = deque(maxlen=_buffer_count * _chunk_size * self._processing_block_count)
        self._data.extend(np.zeros(_chunk_size * _buffer_count))

        self._f0_converter = lambda x: x
        self._mc_converter = lambda x: (x, None)

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
                    param1, param2 = self._mc_converter(mc)
                    # convert_time = time.time() - analyze_time - start_time

                    data = list(itertools.islice(self._data, 0, len(x)))
                    converted = self._synthe.synthesize(data, f0, ap, param1, param2)
                    # finish_time = time.time() - convert_time - start_time
                    # sys.stdout.write("\r %f: %f: %f: %f" % (1., analyze_time,
                    #                                         convert_time, finish_time))
                    self._player.speaker(converted)

        except KeyboardInterrupt:
            self._recorder.terminate()
            self._player.close()

        print("finish")
