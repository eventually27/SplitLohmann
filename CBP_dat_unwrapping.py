# 필요한 라이브러리를 불러옵니다.
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def create_cubic_phase_plate(n, px, c0, wav, r_air, r_mat, delta1, delta2):
    """Create two cubic phase plates and calculate their phase profiles."""
    x = np.arange(-n/2, n/2, 1) * px
    y = np.arange(-n/2, n/2, 1) * px
    x, y = np.meshgrid(x, y)

    h1 = ((x + delta1)**3 + (y + delta1)**3) / c0
    h2 = -((x - delta2)**3 + (y - delta2)**3) / c0

    cubic_phase_plate1 = np.exp(-1j * 2 * np.pi * (h1) * (r_mat - r_air) / wav)
    cubic_phase_plate2 = np.exp(-1j * 2 * np.pi * (h2) * (r_mat - r_air) / wav)

    return cubic_phase_plate1, cubic_phase_plate2

def unwrap_phase(phase):
    """Unwrap the phase to remove discontinuities."""
    return np.unwrap(np.unwrap(phase, axis=0), axis=1)

def plot3d(data, title):
    """Plot 3D surface of the data."""
    x = np.arange(data.shape[0])
    y = np.arange(data.shape[1])
    x, y = np.meshgrid(x, y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, data, rstride=10, cstride=10, cmap='jet')
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Phase')
    ax.set_title(title)
    plt.show()
    
def save_phase2sag_to_file(data):
    output = ""
    output += "1500 1500 0.01 0.01 0 0 0\n" # nx ny px py unit 0 0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            output += "%.9f 0 0 0 0\n" % data[i, j]
    return output

def main():
    n = 1500
    px = 10e-6
    c0 = 0.0193
    wav = 520e-9
    delta1 = 0.00
    delta2 = 0.00
    r_air = 1
    r_mat = 1.456  # fused silica

    cubic_phase_plate1, cubic_phase_plate2 = create_cubic_phase_plate(n, px, c0, wav, r_air, r_mat, delta1, delta2)

    phase1 = np.angle(cubic_phase_plate1)
    phase2 = np.angle(cubic_phase_plate2)

    unwrapped_phase1 = unwrap_phase(phase1) * wav / (2 * np.pi) * 1e+3  # convert to mm
    unwrapped_phase2 = unwrap_phase(phase2) * wav / (2 * np.pi) * 1e+3  # convert to mm

    plot3d(unwrapped_phase1, 'Unwrapped Phase 1')
    plot3d(unwrapped_phase2, 'Unwrapped Phase 2')
    
    phase2sag_text1 = save_phase2sag_to_file(unwrapped_phase1)
    
    with open("CBP1sag.dat", "w") as file:
        file.write(phase2sag_text1)
    

if __name__ == "__main__":
    main()
