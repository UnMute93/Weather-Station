# -*- coding: utf-8 -*-

import time
import threading

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from sense_hat import SenseHat


class Worker(QObject):

    signalStatus = pyqtSignal(str)
    updateButtons = pyqtSignal(bool, bool)
    updateLcd = pyqtSignal(float, float)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.filename = "log.txt"
        self.temperature = 0
        self.humidity = 0
        self.interval = 5
        self.sense = SenseHat()
        self.debugMode = False
        self.stopEvent = threading.Event()

    @pyqtSlot()
    def start(self):
        self.updateButtons.emit(False, True)
        self.stopEvent.clear()
        while not self.stopEvent.is_set():
            if self.debugMode == False:
                self.temperature = self.sense.get_temperature()
                self.humidity = self.sense.get_humidity()

            self.updateLcd.emit(self.temperature, self.humidity)
            self.show_temperature_on_led_matrix(self.temperature)
            self.log_to_file(self.temperature, self.humidity, self.filename)
            self.stopEvent.wait(timeout=(self.interval))

    def stop(self):
        self.stopEvent.set()

    def update_temperature(self, value):
        if self.debugMode == True:
            self.temperature = value

    def update_humidity(self, value):
        if self.debugMode == True:
            self.humidity = value

    def update_interval(self, value):
        self.interval = value

    def update_debug_mode(self, value):
        self.debugMode = value
        if value == True:
            self.filename = "log_debug.txt"
        else:
            self.filename = "log.txt"

    def log_to_file(self, temperature, humidity, filename):
        temperatureString = "{:.1f}°C".format(temperature)
        humidityString = "{:.0f}%".format(humidity)
        timeString = time.strftime("%d/%m/%Y %H:%M:%S")
        file = open(filename, "a")
        file.write(timeString + " | " + "Temperature: " + temperatureString + " | " + "Humidity: " + humidityString
                   + "\n")
        file.close()

    def show_temperature_on_led_matrix(self, temperature):
        temperatureString = "{:.1f}".format(temperature)
        self.sense.show_message(temperatureString + "c")