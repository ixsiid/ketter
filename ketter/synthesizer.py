import numpy as np

class Synthesizer:
    def __init__(self, fs, frame_period, fft_size=1024, mcep_alpha=0.41):
        self.fs = fs
        self.period = frame_period
        self.fft_size = fft_size
        self.mcep_alpha = mcep_alpha

    def synthesize(self, x, f0, ap, param1, param2):
        return np.array([0.])
        