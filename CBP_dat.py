# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 11:44:45 2023

@author: admin
"""

import numpy as np
import matplotlib.pyplot as plt




n = 3333
px = 3.6e-6

x = np.arange(-n/2,n/2,1)*px
y = np.arange(-n/2,n/2,1)*px

x, y = np.meshgrid(x,y)

c0 = 0.0193
wav = 532e-9
delta = 0.000

h1 = ((x+delta)**3 + (y+delta)**3)/ c0
h2 = ((x-delta)**3 + (y-delta)**3)/ c0

r_air = 1
r_mat = 1.456


phase_modulation = np.exp(-1j*2*np.pi*(h1 + h2)*(r_mat - r_air)/wav)

plt.imshow(np.angle(phase_modulation),cmap='gray')

plt.show()
phase_modulation = np.fft.ifftshift(np.fft.ifft2(phase_modulation))

plt.imshow(np.abs(phase_modulation))
plt.show()