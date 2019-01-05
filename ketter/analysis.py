from pyworld import pyworld
import pysptk

class Analysis:
    def __init__(self, fs=16000.0, frame_period=8.0, fft_size=1024, mcep_order=24, mcep_alpha=0.41):
        """Analyze acoustic feature with mel-cepstrum
        Parameters
        ----------
        fs : float
            Sampling rate [Hz]
        frame_period : float
        fft_size : int
        mcep_order : int
            Order of mel-cepstrum
        mcep_alpha : float
            All-pass constant
        Returns
        -------
        """
        self.fs = fs
        self.f0max = 800.0
        self.f0min = 71.0
        self.period = frame_period # milli sec
        self.fft_size = fft_size
        self.mcep_order = mcep_order
        self.mcep_alpha = mcep_alpha

    def analyze(self, data):
        """Analyze acoustic feature with mel-cepstrum
        Parameters
        ----------
        data : float ndarray[-1:1) audio data
        -------
        f0 : array, shape (`T`,)
            F0 sequence
        sp : array, shape (`T`, `fft_size / 2 + 1`)
            Spectral envelope sequence
        ap: array, shape (`T`, `fft_size / 2 + 1`)
            aperiodicity sequence
        mcep : array, shape (`T`, `mcep_order + 1`)
            Mel-cepstrum sequence
        """
        # pyworld.harvest を使うと10倍処理が遅くなる -> リアルタイム変換に難あり
        _f0, time_axis = pyworld.dio(data, self.fs,
                                     f0_floor=self.f0min, f0_ceil=self.f0max,
                                     frame_period=self.period)
        f0 = pyworld.stonemask(data, _f0, time_axis, self.fs)
        ap = pyworld.d4c(data, f0, time_axis, self.fs, fft_size=self.fft_size)
        sp = pyworld.cheaptrick(data, f0, time_axis, self.fs, fft_size=self.fft_size)
        mcep = pysptk.sp2mc(sp, order=self.mcep_order, alpha=self.mcep_alpha)

        return f0, ap, sp, mcep
