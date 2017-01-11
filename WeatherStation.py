# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, QThread, pyqtSignal

from MainWindow import MainWindow
from Worker import Worker


class WeatherStation(QObject):

    signalStatus = pyqtSignal(str)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.window = MainWindow()
        self.worker = Worker()
        self.worker_thread = QThread()
        self.connect_signals()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        self.window.btnCollectOff.setEnabled(False)
        self.window.show()

    def connect_signals(self):
        self.window.dbmTemperature.valueChanged.connect(self.worker.update_temperature)
        self.window.dbmHumidity.valueChanged.connect(self.worker.update_humidity)
        self.window.dbmPressure.valueChanged.connect(self.worker.update_pressure)
        self.window.dbmInterval.valueChanged.connect(self.worker.update_interval)
        self.window.checkDebug.stateChanged.connect(self.update_debug_status)
        self.window.btnCollectOn.clicked.connect(self.worker.start)
        self.window.btnCollectOff.clicked.connect(self.worker_reset)

        self.parent().aboutToQuit.connect(self.worker_quit)

        self.worker.updateButtons.connect(self.update_buttons)
        self.worker.updateLcd.connect(self.update_lcd)
        self.worker.updateGraphs.connect(self.update_graphs)

    def worker_reset(self):
        if self.worker_thread.isRunning():
            self.update_buttons(True, False)
            self.worker.stop()

    def worker_quit(self):
        if self.worker_thread.isRunning():
            self.worker.stop()

    def update_buttons(self, onEnabled, offEnabled):
        self.window.btnCollectOn.setEnabled(onEnabled)
        self.window.btnCollectOff.setEnabled(offEnabled)

    def update_lcd(self, temperature, humidity, pressure):
        self.window.lcdTemperature.display(temperature)
        self.window.lcdHumidity.display(humidity)
        self.window.lcdPressure.display(pressure)

    def update_debug_status(self):
        if self.window.checkDebug.isChecked() == True:
            self.worker.update_debug_mode(True)
        else:
            self.worker.update_debug_mode(False)

    def update_graphs(self, temperature, humidity, pressure, time):
        self.window.temperatureGraph.update_figure(temperature, time)
        self.window.humidityGraph.update_figure(humidity, time)
        self.window.pressureGraph.update_figure(pressure, time)