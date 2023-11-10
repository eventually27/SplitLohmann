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
phase2sag = np.angle(phase_modulation)*wav/(2*np.pi) * 1e+3

plt.imshow(phase2sag,cmap='gray')
plt.show()

phase_modulation = np.fft.ifftshift(np.fft.ifft2(phase_modulation))

plt.imshow(np.abs(phase_modulation))
plt.show()

def save_phase2sag_to_file(data):
    output = ""
    output += "3333 3333 0.036 0.036 0 0 0\n"
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            output += "%f 0 0 0 0\n" % data[i, j]
    return output

phase2sag_text = save_phase2sag_to_file(phase2sag)

with open("grid_data.dat", "w") as file:
    file.write(phase2sag_text)

# #dat 파일 생성 phase to sag"
# data = """10 10 0.036 0.036 0 0 0
# 1 0 0 0 0
# 0 0 0 0 0
# 1 0 0 0 0
# 1 0 0 0 0
# 0 0 0 0 0
# 1 0 0 0 0
# 1 0 0 0 0
# 1 0 0 0 0
# 0 0 0 0 0
# 1 0 0 0 0"""

# with open("data.dat", "w") as file:
#     file.write(data)