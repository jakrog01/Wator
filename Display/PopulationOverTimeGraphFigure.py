import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import numpy as np

class PopulationOverTimeGraphFigure(FigureCanvasQTAgg):
    def __init__(self, AreaSize):
        fig = Figure(figsize=(AreaSize, AreaSize), dpi=100)
        fig.subplots_adjust(left=0.2, bottom = 0.15)
        self.__axes = fig.add_subplot(111)
        super(PopulationOverTimeGraphFigure, self).__init__(fig)
        self.__xs = []
        self.__ysprey = []
        self.__yspredator = []
        self.__alphas = np.linspace(0.1, 1, 35)

    def plot(self, yprey, ypredators):
        self.__axes.cla()

        if len(self.__xs) < 35:
            self.__ysprey.append(yprey)
            self.__yspredator.append(ypredators)
            if len(self.__xs) == 0:
                self.__xs.append(0)
            else:
                self.__xs.append(max(self.__xs) + 1)
        else:
            ysprey = self.__ysprey[1:]
            ysprey.append(yprey)
            self.__ysprey = ysprey

            yspredator = self.__yspredator[1:]
            yspredator.append(ypredators)
            self.__yspredator = yspredator

        self.__axes.set_xticks([])
        self.__axes.set_ylabel("Population", fontsize = 8)
        self.__axes.set_xlabel("Time", fontsize = 8)
        self.__axes.set_xlim(0, 40)
        self.__axes.tick_params(axis='both', which='major', labelsize=5)
        self.__axes.set_ylim(0, max(max(self.__yspredator) + 250, max(self.__ysprey) + 250))
        self.__axes.scatter(self.__xs, self.__ysprey, color = "blue", alpha=self.__alphas, s = 20)
        self.__axes.scatter(self.__xs, self.__yspredator, color = "red", alpha=self.__alphas, s= 20)