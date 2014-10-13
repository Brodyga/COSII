#import math
#import cmath
import numpy as np
import matplotlib.pyplot as plt

N = 1024
period = 2 * np.pi

count = 0

def func(x):
    return (np.sin(x) + np.cos(x))

def func_y(x):
    return (np.cos(x))

def func_z(x):
    return (np.sin(x))

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

def convolution(x, num):
    y = func(x)
    if num == 1:
        z = func_y(x)
    else:
        z = func_z(x)

    N = len(y)

    res = [0] * N

    m = 0
    while (m < N):
        h = 0
        while (h < N):
            if (m - h >= 0):
                res[m] += y[h] * z[m - h]
            else:
                res[m] += y[h] * z[m - h + N]

            h += 1

        res[m] /= N
        m += 1

    return res

def correlation(x, num):
    y = func(x)
    if num == 1:
        z = func_y(x)
    else:
        z = func_z(x)

    N = len(y)

    res = [0] * N

    m = 0
    while (m < N):
        h = 0
        while (h < N):
            if (m + h < N):
                res[m] += y[h] * z[m + h]
            else:
                res[m] += y[h] * z[m + h - N]

            h += 1

        res[m] /= N
        m += 1

    return res

def convolution_TFFT(x, num):
    y = func(x)
    if num == 1:
        z = func_y(x)
    else:
        z = func_z(x)

    res_y = TFFT(y, 1)
    res_z = TFFT(z, 1)

    N = len(res_y)
    res_fft = [0] * N
    i = 0
    while (i < N):
        res_fft[i] = res_y[i] * res_z[i] / (N * N)
        i += 1

    res = TFFT(res_fft, -1)

    return res

def correlation_TFFT(x, num):
    y = func(x)
    if num == 1:
        z = func_y(x)
    else:
        z = func_z(x)

    res_y = TFFT(y, 1)
    res_z = TFFT(z, 1)

    N = len(res_y)
    i = 0
    while (i < N):
        res_y[i] = res_y[i].conjugate() / (N * N)
        i += 1

    res_fft = [0] * N
    i = 0
    while (i < N):
        res_fft[i] = res_y[i] * res_z[i]
        i += 1

    res = TFFT(res_fft, -1)
    return res

x = np.arange(0, period, period/N)
y = func(x)

corr = correlation(x, 1)
corr_fft = correlation_TFFT(x, 1)
conv = convolution(x, 1)
conv_fft = convolution_TFFT(x, 1)

corr1 = correlation(x, -1)
corr_fft1 = correlation_TFFT(x, -1)
conv1 = convolution(x, -1)
conv_fft1 = convolution_TFFT(x, -1)

fig, axes = plt.subplots(nrows=2, ncols=6, figsize=(6,6))

axes[0, 0].plot(x, y, 'r')
axes[0, 1].plot(x, func_y(x), 'brown')
axes[0, 2].plot(x, corr, 'g')
axes[0, 3].plot(x, corr_fft, 'blue')
axes[0, 4].plot(x, conv, 'black')
axes[0, 5].plot(x, conv_fft, 'pink')

axes[1, 0].plot(x, y, 'r')
axes[1, 1].plot(x, func_z(x), 'brown')
axes[1, 2].plot(x, corr1, 'g')
axes[1, 3].plot(x, corr_fft1, 'blue')
axes[1, 4].plot(x, conv1, 'black')
axes[1, 5].plot(x, conv_fft1, 'pink')

plt.show()