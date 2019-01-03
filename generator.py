import numpy as np


class Generator:
    def sin(self, A, f0, fs, length):
        """
            振幅A,基本周波数f0, サンプリング周波数fs,再生時間length秒の正弦波を作成して返す
        """

        data = []
        for n in range(int(length * fs)):
            s = A * np.sin(2 * np.pi * f0 * n / fs)  # 正弦波の計算

            # 振幅の範囲を-1～1に設定
            if s > 1.0: s = 1.0
            if s < -1.0: s = -1.0
            data.append(s)

        return data