import numpy as np
import scipy.linalg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools

def main():
    # Generate Data...
    numdata = 100
    x = np.random.random(numdata)
    y = np.random.random(numdata)
    z = x**2 + y**2 + 3*x**3 + y + np.random.random(numdata)

    # Fit a 3rd order, 2d polynomial
    m = polyfit2d(x,y,z)

    # Evaluate it on a grid...
    nx, ny = 20, 20
    xx, yy = np.meshgrid(np.linspace(x.min(), x.max(), nx), 
                         np.linspace(y.min(), y.max(), ny))
    zz = polyval2d(xx, yy, m)

    # Plot
    #plt.imshow(zz, extent=(x.min(), y.max(), x.max(), y.min()))
    #plt.scatter(x, y, c=z)
    #plt.show()

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z, color='red', zorder=0)
    ax.plot_surface(xx, yy, zz, zorder=10)
    ax.set_xlabel('X data')
    ax.set_ylabel('Y data')
    ax.set_zlabel('Z data')

    plt.show()
    text = "filler"

def polyfit2d(x, y, z, order=4):
    ncols = (order + 1)**2
    G = np.zeros((x.size, ncols))
    #ij = itertools.product(range(order+1), range(order+1))
    ij = xy_powers(order)
    for k, (i,j) in enumerate(ij):
        G[:,k] = x**i * y**j
    m, _, _, _ = np.linalg.lstsq(G, z)
    return m

def polyval2d(x, y, m):
    order = int(np.sqrt(len(m))) - 1
    #ij = itertools.product(range(order+1), range(order+1))
    ij = xy_powers(order)
    z = np.zeros_like(x)
    for a, (i,j) in zip(m, ij):
        z += a * x**i * y**j
    return z

def xy_powers(order):
    powers = itertools.product(range(order + 1), range(order + 1))
    return [tup for tup in powers if sum(tup) <= order]

main()