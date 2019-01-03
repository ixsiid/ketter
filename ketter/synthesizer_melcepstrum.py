from pyworld import pyworld
import pysptk
from .synthesizer import Synthesizer

class SynthesizerMelcepstrum(Synthesizer):
    def synthesize(self, x, f0, ap, mcep, _):
        sp = pysptk.mc2sp(mcep, self.mcep_alpha, self.fft_size)
        return pyworld.synthesize(f0, sp, ap, self.fs, frame_period=self.period)
        