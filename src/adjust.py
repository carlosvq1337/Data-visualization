import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time
from os import listdir
from os.path import isfile, join
import argparse
import sys

plt.rcParams.update({'font.size': 15})
plt.ion()
class DynamicUpdate():
    
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        f = open(path_to_file)
        lines = f.readlines()
        line_0 = lines[0].split(' ')
        line_0 = [i for i in line_0 if i != '']
        self.xlabel = line_0[0].replace('_', ' ')
        self.ylabel1 = line_0[1].replace('_', ' ')
        self.ylabel2 = line_0[2].replace('_', ' ')
        self.fig_title = line_0[3].replace('_', ' ')
        self.iter = ""
        self.value = ""
        f.close()


    def get_len(self):
        with open(self.path_to_file) as f:
            for i,l in enumerate(f):
                pass
        return i+1

    def update_data(self):
        self.x_data = []
        self.R_exp = []
        self.R_adj = []
        self.Im_exp = []
        self.Im_adj = []
        f = open (self.path_to_file, "r")
        lines = f.readlines()
        line_1 = lines[1].split(' ')
        line_1 = [i for i in line_1 if i != '']
        self.iter = line_1[0]
        self.value = line_1[1].strip()
        for x in range (2, self.get_len()):
            line = lines[x].split(' ')
            line = [i for i in line if i != '' and i != '\n']
            self.x_data.append(float(line[0]))
            self.R_exp.append(float(line[1]))
            self.R_adj.append(float(line[2]))
            self.Im_exp.append(float(line[3]))
            self.Im_adj.append(float(line[4]))
        f.close()


    def on_launch(self):
        #Set up plot
        self.figure, self.ax = plt.subplots(1,2)
        self.figure.suptitle(self.fig_title)
        self.lines = [self.ax[0].plot([],[], "or", alpha = 0.3, label = "Experimental"), self.ax[0].plot([],[], linewidth = 3, label = "Fitting"), self.ax[1].plot([],[], "or", alpha = 0.3, label = "Experimental"), self.ax[1].plot([],[], linewidth = 3, label = "Fitting")]
        #Autoscale on unknown axis and known lims on the other
        self.ax[0].set_autoscaley_on(True)
        self.ax[0].set_autoscalex_on(True)
        self.ax[0].set_yscale("log")
        self.ax[0].set_ylabel(self.ylabel1)
        self.ax[0].set_xlabel(self.xlabel)
        self.ax[0].legend(loc = "upper right", prop={'size': 15})


        self.ax[1].set_autoscaley_on(True)
        self.ax[1].set_autoscalex_on(True)
        self.ax[1].set_yscale("log")
        self.ax[1].set_xlabel(self.xlabel)
        self.ax[1].set_ylabel(self.ylabel2)
        self.ax[1].legend(loc = "upper right", prop={'size': 15})



        #Other stuff
        self.ax[0].grid()
        self.ax[1].grid()
        ...

    def on_running(self):
        self.figure.suptitle(self.fig_title + "(" + self.iter + ", " + self.value + ")")



        #Update data (with the new _and_ the old points)
        self.lines[0][0].set_xdata(self.x_data)
        self.lines[0][0].set_ydata(self.R_exp)

        self.lines[1][0].set_xdata(self.x_data)
        self.lines[1][0].set_ydata(self.R_adj)


        self.lines[2][0].set_xdata(self.x_data)
        self.lines[2][0].set_ydata(self.Im_exp)

        self.lines[3][0].set_xdata(self.x_data)
        self.lines[3][0].set_ydata(self.Im_adj)

        #Need both of these in order to rescale
        self.ax[0].relim()
        self.ax[0].autoscale_view()
        self.ax[1].relim()
        self.ax[1].autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    #Example
    def __call__(self):
        self.on_launch()
        while True:
            self.update_data()
            self.on_running()
            time.sleep(0.25)


if __name__ == "__main__":
    dyn = DynamicUpdate(sys.argv[1])
    dyn()
    