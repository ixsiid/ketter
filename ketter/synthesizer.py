from pyworld import pyworld
import pysptk

class Synthesizer:
    def __init__(self, fs, frame_period, fft_size=1024, mcep_alpha=0.41):
        self.fs = fs
        self.period = frame_period
        self.fft_size = fft_size
        self.mcep_alpha = mcep_alpha

    def synthesize(self, f0, sp, ap, mcep=None):
        if mcep is not None:
            sp = pysptk.mc2sp(mcep, self.mcep_alpha, self.fft_size)


        return pyworld.synthesize(f0, sp, ap, self.fs, frame_period=self.period)
        