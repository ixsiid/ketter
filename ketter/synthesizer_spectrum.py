from pyworld import pyworld
from .synthesizer import Synthesizer

class SynthesizerSpectrum(Synthesizer):
    def synthesize(self, x, f0, ap, sp, _):
        return pyworld.synthesize(f0, sp, ap, self.fs, frame_period=self.period)
        