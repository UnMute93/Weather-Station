# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow

import ui_weather_station

import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams

class CustomCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.valueList = []
        self.timeList = []
        self.time = 0
        self.ylabel = ""

    def update_figure(self, value, time):
        self.time += time
        self.valueList.append(value)
        self.timeList.append(self.time)
        if len(self.valueList) >= 10:
            del self.valueList[0]
            del self.timeList[0]

        self.axes.plot(self.timeList, self.valueList , 'b-', linewidth=5)
        self.axes.set_xlabel("Seconds")
        self.axes.set_ylabel(self.ylabel)
        self.axes.locator_params(nbins=5)
        self.draw()

class MainWindow(QMainWindow, ui_weather_station.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        rcParams.update({'figure.autolayout': True})
        plotLayout = QtWidgets.QVBoxLayout(self.widget)
        self.temperatureGraph = CustomCanvas(self.widget, width=5, height=4, dpi=100)
        self.humidityGraph = CustomCanvas(self.widget, width=5, height=4, dpi=100)
        self.pressureGraph = CustomCanvas(self.widget, width=5, height=4, dpi=100)
        self.temperatureGraph.ylabel = "Temp (°C)"
        self.humidityGraph.ylabel = "Hum (%)"
        self.pressureGraph.ylabel = "Pres (mbar)"
        plotLayout.addWidget(self.temperatureGraph)
        plotLayout.addWidget(self.humidityGraph)
        plotLayout.addWidget(self.pressureGraph)