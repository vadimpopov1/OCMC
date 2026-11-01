import numpy as np
import matplotlib.pyplot as plt
from math import *

def fourie_transform(x):
    N = len(x)
    X = []
    for i in range(N):
        sum = 0
        for k in range(N):
            sum += x[k] * np.exp(-2j * np.pi * i * (k / N))
        X.append(sum)
    return X

f = 15

# 1 (Вывести график по варианту)
x = np.linspace(0, 1, 1000)
y = 6 * np.sin(2 * np.pi * f * x + (np.pi / 10))

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, y)
ax.set_xlabel('t (с)')
ax.set_ylabel('A')
ax.grid()
plt.show()

# 2-3 (Определить максимальную частоту в спектре + определить  минимальную необходимую  частоту)
max_freq = f
min_freq_kotelnikov = f * 2

print(max_freq, min_freq_kotelnikov)

# 4 (Оцифровать сигнал с полученной частотой дискретизации)
k = 1
fs = min_freq_kotelnikov * k

n_samples = int(fs * 1.0) 
x_sampled = np.linspace(0, 1.0, n_samples, endpoint=False)
y_sampled = 6 * np.sin(2 * np.pi * f * x_sampled + (np.pi / 10))

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, y)
ax.plot(x_sampled, y_sampled)
ax.set_xlabel('t (с)')
ax.set_ylabel('A')
ax.grid()
plt.show()

# 5 (Преобразование Фурье)
y_sampled_ft = fourie_transform(y_sampled)
len_y_sampled_ft = len(y_sampled_ft)

freq = np.arange(len_y_sampled_ft) * fs / len_y_sampled_ft 
amp = np.abs(y_sampled_ft) / len_y_sampled_ft

half_len = len_y_sampled_ft // 2 + 1
freq = freq[:half_len]
amp = amp[:half_len]

spectrum_width = fs / 2
memory_bytes = y_sampled.nbytes

print(f"Ширина спектра (k=1): {spectrum_width} Гц")
print(f"Объем памяти (k=1): {memory_bytes} байт")

# 6 (Восстановление сигнала)
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, y)
ax.plot(x_sampled, y_sampled) 
ax.plot(x_sampled, y_sampled, 'ro')
ax.set_xlabel('t (с)')
ax.set_ylabel('A')
ax.grid()
plt.show()

# 7 (Увеличить частоту дискретизации в 4 раза + 4-6)
k_new = 4
fs_new = min_freq_kotelnikov * k_new

n_samples_new = int(fs_new * 1.0) 
x_sampled_new = np.linspace(0, 1.0, n_samples_new, endpoint=False)
y_sampled_new = 6 * np.sin(2 * np.pi * f * x_sampled_new + (np.pi / 10))

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, y)
ax.plot(x_sampled_new, y_sampled_new)
ax.set_xlabel('t (с)')
ax.set_ylabel('A')
ax.grid()
plt.show()

# (Новое преобразование Фурье)
y_sampled_ft_new = fourie_transform(y_sampled_new)
len_y_sampled_ft_new = len(y_sampled_ft_new)

freq_new = np.arange(len_y_sampled_ft_new) * fs_new / len_y_sampled_ft_new 
amp_new = np.abs(y_sampled_ft_new) / len_y_sampled_ft_new

half_len_new = len_y_sampled_ft_new // 2 + 1
freq_new = freq_new[:half_len_new]
amp_new = amp_new[:half_len_new]

spectrum_width_new = fs_new / 2
memory_bytes_new = y_sampled_new.nbytes

print(f"Ширина спектра (k=4): {spectrum_width_new} Гц")
print(f"Объем памяти (k=4): {memory_bytes_new} байт")

# (Новое восстановление сигнала)
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, y)
ax.plot(x_sampled_new, y_sampled_new) 
ax.plot(x_sampled_new, y_sampled_new, 'ro')
ax.set_xlabel('t (с)')
ax.set_ylabel('A')
ax.grid()
plt.show()
