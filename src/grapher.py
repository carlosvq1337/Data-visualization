#! python3

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time
from os import listdir
from os.path import isfile, join
import argparse
import sys

plt.ion()

class DynamicUpdate():

    def __init__(self, path_to_dir, max_col):
        self.path_to_dir = path_to_dir
        self.paths_to_files = []
        self.x_labels = []
        self.y_labels = []
        self.max_col = int(max_col)
        self.onlyfiles = [f for f in listdir(path_to_dir) if isfile(join(path_to_dir, f))]
        for file in self.onlyfiles:
            if file != "flags":
                self.paths_to_files.append(path_to_dir + "/" + file)
                f = open(path_to_dir + "/" + file, "r")
                lines = f.readlines()
                linex = lines[0].split(' ')
                linex = [i for i in linex if i != '']
                self.x_labels.append(linex[0])
                self.y_labels.append(linex[1])
                f.close()
            else:
                self.flag = linex[0]
                self.path_to_flags = path_to_dir + "/" + file
        self.min_x = 1
        self.max_x = 2000
        self.number_of_lines = self.get_lines()
        self.dct = {}
        self.number_of_files = len(self.paths_to_files)

    def update_data(self):
        self.number_of_lines = self.get_lines()
        for file_path in self.paths_to_files:
            y_values = []
            x_values = []
            f = open(file_path, "r")
            lines = f.readlines()
            for x in range(1, self.number_of_lines):
                linex = lines[x].split(' ')
                linex = [i for i in linex if i != '' and i != '\n']
                x_values.append(float(linex[0].strip()))
                y_values.append(float(linex[1].strip()))
            self.dct[self.y_labels[self.paths_to_files.index(file_path)]] = y_values
            self.dct[self.x_labels[self.paths_to_files.index(file_path)]] = x_values
            f.close()

        f = open(self.path_to_flags, "r")
        lines = f.readlines()
        self.flag = lines[0]

    def get_lines (self): #gets the number of lines in the file with least lines (to prevent errors)
        min_lines = 99999
        for file_path in self.paths_to_files:
            with open(file_path) as f:
                for i, l in enumerate(f):
                    pass
            f.close()
            if i + 1 < min_lines:
                min_lines = i + 1
        return min_lines


    def on_launch(self):
    
        #determine dimensions of figure
        if self.number_of_files < self.max_col:
            self.rows = []
            self.rows.append(self.number_of_files)
            
            self.figure, self.ax = plt.subplots(len(self.rows),self.rows[0])
            self.lines = []
            for c in range(0, self.rows[0]):
                self.lines.append(self.ax[c].plot([],[]))
                
                #Autoscale on unknown axis and known lims on the other
                self.ax[c].set_autoscaley_on(True)
                self.ax[c].set_titlel(self.y_labels[c])
                if self.flag == "1":
                    self.ax[c].set_xscale("log")

                self.ax[c].axes.get_yaxis().set_visible(False)
                self.ax[c].axes.get_xaxis().set_visible(False)
                #Other stuff
                
                self.ax[c].grid()


        else:
            if self.number_of_files%self.max_col == 0:
                self.rows = [self.max_col]*(int(self.number_of_files/self.max_col))
            else:
                self.rows = [self.max_col]*(int(self.number_of_files/self.max_col))
                self.rows.append(self.number_of_files%self.max_col)


            #Set up plot
            self.figure, self.ax = plt.subplots(len(self.rows),self.rows[0])
            self.lines = []
            for r in range (0, len(self.rows)):
                for c in range(0, self.rows[r]):
                    self.lines.append(self.ax[r][c].plot([],[]))
                
                    #Autoscale on unknown axis and known lims on the other
                    self.ax[r][c].set_autoscaley_on(True)
                    self.ax[r][c].set_title(self.y_labels[c+self.max_col*r])
                    self.ax[r][c].axes.get_yaxis().set_visible(False)
                    self.ax[r][c].axes.get_xaxis().set_visible(False)
                    if self.flag == "1":
                        self.ax[r][c].set_xscale("log")
                    if self.flag == "0":
                        self.ax[r][c].set_xscale("linear")
                    #Other stuff
                
                    self.ax[r][c].grid()

            if self.number_of_files%self.max_col != 0:
                for c in range(self.rows[len(self.rows)-1], self.max_col):
                    self.ax[len(self.rows)-1][c].axes.get_yaxis().set_visible(False)
                    self.ax[len(self.rows)-1][c].axes.get_xaxis().set_visible(False)
                    self.ax[len(self.rows)-1][c].grid()


    def on_running(self):
        if self.flag == "1":
            self.figure.suptitle("APCSA Fitting" + ": " + str(self.get_lines() - 1) + " WITH LOG SCALE ON X", fontsize = 15)   
        if self.flag == "0":
            self.figure.suptitle("APCSA Fitting" + ": " + str(self.get_lines() - 1) + " WITH LINEAR SCALE ON X", fontsize = 15)   
        if self.number_of_files < self.max_col:
            for c in range(0,self.rows[0]):
                self.lines[c][0].set_xdata(self.dct[self.x_labels[c]])
                self.lines[c][0].set_ydata(self.dct[self.y_labels[c]])

                
                #Need both of these in order to rescale
                self.ax[c].relim()
                self.ax[c].autoscale_view()
        
        
        else:
            #Update data (with the new _and_ the old points)
            for r in range (0, len(self.rows)):
                for c in range(0,self.rows[r]):

                    self.lines[c+self.max_col*r][0].set_xdata(self.dct[self.x_labels[c+self.max_col*r]])
                    self.lines[c+self.max_col*r][0].set_ydata(self.dct[self.y_labels[c+self.max_col*r]])
                    self.ax[r][c].set_title(self.y_labels[c+self.max_col*r] + " =" + str(self.dct[self.y_labels[c+self.max_col*r]][-1]), fontsize =8)
                    if self.flag == "1":
                        self.ax[r][c].set_xscale("log")
                    if self.flag == "0":
                        self.ax[r][c].set_xscale("linear")
                    #Need both of these in order to rescale
                    self.ax[r][c].relim()
                    self.ax[r][c].autoscale_view()

        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    #Example
    def __call__(self):
        self.on_launch()
        while self.number_of_lines < self.max_x:
            self.update_data()
            self.on_running()
            time.sleep(0.25)


if __name__ == "__main__":
    dyn = DynamicUpdate(sys.argv[1], sys.argv[2])
    dyn()
    