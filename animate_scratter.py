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
        
        self.fig, self.ax = plt.subplots()
        
        self.c = col # colour
        self.func = func
        self.t = t
        self.iteration = 0
        
        #init whitespace
        self.x = np.arange(self.xmin, self.xmax + resolution, resolution)
        self.y = np.arange(self.ymin, self.ymax + resolution, resolution)
        xx, yy = np.meshgrid(self.x, self.y, sparse=True)
        self.z = self.func(xx, yy)
        self.update(pos)

        
    def draw_background(self):
        self.ax.contourf(self.x, self.y, self.z)
    
    
    def update_canvas(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


    def update(self, pos):
        self.ax.clear()
        self.ax.axis([self.xmin, self.xmax, self.ymin, self.ymax])
        self.draw_background()
        self.ax.scatter(pos[:, 0], pos[:, 1], s=30, c=self.c)
        
        # Display the current loop iteration
        self.ax.text(0.95, 0.05, f'Iteration: {self.iteration}', 
                     verticalalignment='bottom', horizontalalignment='right',
                     transform=self.ax.transAxes, 
                     color='black', fontsize=12, fontweight='bold')
        
        self.update_canvas()
        time.sleep(self.t)
        
        self.iteration += 1  # Increment the iteration counter
        