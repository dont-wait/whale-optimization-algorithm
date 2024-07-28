import time
import numpy as np
import matplotlib.pyplot as plt


class AnimateScatter():
    def __init__(self, xmin, xmax, ymin, ymax, pos, col, func, resolution, t):
        plt.ion()
        
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        
        self.fig, self.ax = plt.subplots
        
        self.c = col # colour
        self.func = func
        self.t = t
        
        #init whitespace
        self.x = np.arange(self.xmin, self.xmax + resolution, resolution)
        self.y = np.arange(self.ymin, self.ymax + resolution, resolution)
        xx, yy = np.meshgrid(self.x, self.y, sparse=True)
        self.z = self.func(xx, yy)
        self.update(pos)
        
    def draw_background(self):
        self.ax.contourf(self.x, self.y, self.z)
        