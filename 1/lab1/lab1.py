import math
import cmath
import numpy as np
import matplotlib.pyplot as plt

N = 1024
period = 2 * np.pi

count = 0

def func(x):
    return (np.sin(x) + np.cos(x))

def DFT(ValueVector, dir):
    global count
    if dir != 1 :
        if dir != -1 : return 0

    N = len(ValueVector)
    Output = [0] * N

    k = 0
    while(k < N):
        m = 0
        while(m < N):
            Output[k] += ValueVector[m] * np.exp(-dir * 2j * np.pi * k * m / N)
            count += 1
            m += 1

        if dir == 1:
            Output[k] /= N
        k += 1

    return Output

def W(n, N, dir):
  return np.exp(-1j * dir * 2 * np.pi * n/N)

def TFFT(x, dir):
    global count
    N = len(x)
    if N <= 1:
        return x
    even = TFFT(x[0::2], dir)
    odd = TFFT(x[1::2], dir)

    for n in xrange(N/2):
        count += 1
    return [even[n] + W(n, N, dir) * odd[n] for n in xrange(N/2)] + \
           [even[n] - W(n, N, dir) * odd[n] for n in xrange(N/2)]

x = np.arange(0, period, period/N)
y = func(x)

count = 0
y_dft = DFT(y, 1)
print 'DFT', count
dft_abs = map(abs, y_dft)
dft_phase = map(cmath.phase, y_dft)
y_idft = np.real(DFT(y_dft, -1))

count = 0
y_fft = TFFT(y, 1)
print 'FFT ', count
fft_abs = map(abs, np.divide(y_fft, N))
fft_phase = map(cmath.phase, y_fft)
y_ifft = np.real(np.divide(TFFT(y_fft, -1), N))

fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(6,6))

axes[0,0].plot(x, y, 'r')
axes[0,1].plot(x, dft_abs, 'g')
axes[0,2].plot(x, dft_phase, 'blue')
axes[0,3].plot(x, y_idft, 'black')

axes[1,0].plot(x, y, 'r')
axes[1,1].plot(x, fft_abs, 'g')
axes[1,2].plot(x, fft_phase, 'blue')
axes[1,3].plot(x, y_ifft, 'black')

plt.show()