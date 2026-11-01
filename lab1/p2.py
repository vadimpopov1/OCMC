import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

fs, y_voice = wavfile.read("voice.wav")

duration = y_voice.shape[0] / fs
fd = y_voice.shape[0] / duration

print(f"Частота дискретизации (fs): {fs} Гц")
print(f"Математически вычисленная частота дискретизации (fd): {fd} Гц")
print(f"Длительность записи: {duration} сек")
print(f"Количество элементов в файле: {y_voice.shape}")

# 11 (Оставляем каждый 10й отсчет)
y1 = y_voice[::10]
fs1 = fs // 10

wavfile.write("voice_downsampled.wav", fs1, y1.astype(y_voice.dtype))

# 12 (Прямое дискретное преобразование Фурье)
fft_orig = np.fft.rfft(y_voice)
freqs_orig = np.fft.rfftfreq(len(y_voice), d=1/fs)
magnitudes_orig = np.abs(fft_orig)

fft_down = np.fft.rfft(y1)
freqs_down = np.fft.rfftfreq(len(y1), d=1/fs1)
magnitudes_down = np.abs(fft_down)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(freqs_orig[5:], magnitudes_orig[5:])
ax.plot(freqs_down[5:], magnitudes_down[5:])
ax.set_xlabel("Freq, Гц")
ax.set_ylabel("A")
ax.grid()
plt.show()

# 13 (Оценка влияния разрядности АЦП на спектр сигнала)
def adc(y, razr):
    levels = (2**razr) - 1
    y_min, y_max = np.min(y), np.max(y)
    y_norm = (y - y_min) / (y_max - y_min)
    y_quant = np.clip(np.round(y_norm * levels), 0, levels)
    y_restored = y_quant / levels * (y_max - y_min) + y_min
    return y_restored

f_sin = 15
fs_sin = 120
t_sin = np.linspace(0, 1.0, fs_sin, endpoint=False)
y_sin = 6 * np.sin(2 * np.pi * f_sin * t_sin + (np.pi / 10))

for raz in [3, 4, 5, 6]:
    y3 = adc(y_sin, raz)
    mean_err = np.mean(np.abs(y_sin - y3))
    print(f"{raz} бит: ср. ошибка квантования = {mean_err}")

    fft_init = np.fft.rfft(y_sin)
    fft_q = np.fft.rfft(y3)
    freqs_q = np.fft.rfftfreq(len(y_sin), d=1/fs_sin)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(freqs_q, np.abs(fft_init))
    ax.plot(freqs_q, np.abs(fft_q))
    ax.set_title(f"{raz} бит: ср. ошибка квантования: {mean_err}")
    ax.set_xlabel("Freq, Гц")
    ax.set_ylabel("A")
    ax.grid()
    plt.show()