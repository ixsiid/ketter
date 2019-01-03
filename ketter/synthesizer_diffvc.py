from .synthesizer import Synthesizer
import pysptk
from pysptk.synthesis import MLSADF
import numpy as np

class SynthesizerDiffVC(Synthesizer):
    def synthesize(self, x, f0, ap, diff_mcep, refer_mcep):
        alpha = 0.41
        dim = diff_mcep.shape[1] - 1
        shiftl = int(self.fs / 1000 * self.period)
        b = np.apply_along_axis(pysptk.mc2b, 1, diff_mcep, alpha)
        mlsa_fil = pysptk.synthesis.Synthesizer(MLSADF(dim, alpha), shiftl)
        wav = mlsa_fil.synthesis(x, b)
        return wav
        