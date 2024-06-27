# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 11:44:45 2023

@author: admin
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

n = 1500 # 15mm/10um
px = 10e-6

x = np.arange(-n/2,n/2,1)*px
y = np.arange(-n/2,n/2,1)*px

x, y = np.meshgrid(x,y)

c0 = 0.0193
wav = 520e-9
delta1 = 0.00
delta2 = 0.00

h1 = ((x+delta1)**3 + (y+delta1)**3)/ c0
h2 = -((x-delta2)**3 + (y-delta2)**3)/ c0

r_air = 1
r_mat = 1.456 # fused silica


cubic_phase_plate1 = np.exp(-1j*2*np.pi*(h1)*(r_mat - r_air)/wav)
cubic_phase_plate2 = np.exp(-1j*2*np.pi*(h2)*(r_mat - r_air)/wav)

cubic_phase_plate_pair = cubic_phase_plate1 * cubic_phase_plate2
phase2sag1 = np.angle(cubic_phase_plate1)*wav/(2*np.pi) * 1e+3 #unit mm
phase2sag2 = np.angle(cubic_phase_plate2)*wav/(2*np.pi) * 1e+3 #unit mm

plt.subplot(1,4,1)
plt.imshow(np.angle(cubic_phase_plate1),cmap='gray')
plt.axis('off')
plt.subplot(1,4,2)
plt.imshow(np.angle(cubic_phase_plate2),cmap='gray')
plt.axis('off')
plt.subplot(1,4,3)
plt.imshow(np.angle(cubic_phase_plate_pair),cmap='gray')
plt.axis('off')
phase_modulation = np.fft.ifftshift(np.fft.ifft2(cubic_phase_plate_pair))
plt.subplot(1,4,4)
plt.imshow(np.abs(phase_modulation))
plt.show()

def plot3d(data):
    x = np.arange(data.shape[0])
    y = np.arange(data.shape[1])
    x, y = np.meshgrid(x, y)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, data, rstride = 1, cstride = 1, cmap='jet')
    
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Phase')
    ax.set_title('3D Plot of Phase Data')
    
    # 플롯 표시
    plt.show()

def save_phase2sag_to_file(data):
    output = ""
    output += "1500 1500 0.01 0.01 0 0 0\n" # nx ny px py unit 0 0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            output += "%.9f 0 0 0 0\n" % data[i, j]
    return output

# def save_phase2sag_to_file(data):
#     output = ""
#     # output += "3333 3333 0.0036 0.0036 0 0 0\n" # nx ny px py unit 0 0
#     for i in range(data.shape[0]):
#         for j in range(data.shape[1]):
#             output += "%.9f .9f .9f\n" % {data[i, j],x[i,j],y[i,j]}
#     return output

if __name__=="__main__":
    
    plot3d(phase2sag1)
    # plot3d(phase2sag2)
    
    phase2sag_text1 = save_phase2sag_to_file(phase2sag1)
    
    with open("CBP1sag.dat", "w") as file:
        file.write(phase2sag_text1)
    
    phase2sag_text2 = save_phase2sag_to_file(phase2sag2)
    
    with open("CBP2sag.dat", "w") as file:
        file.write(phase2sag_text2)