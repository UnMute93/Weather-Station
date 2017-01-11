# -*- coding: utf-8 -*-

import time
import threading

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from sense_hat import SenseHat


class Worker(QObject):
    signalStatus = pyqtSignal(str)
    updateButtons = pyqtSignal(bool, bool)
    updateLcd = pyqtSignal(float, float, float)
    updateGraphs = pyqtSignal(float, float, float, float)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.filename = "log.txt"
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        self.interval = 5
        self.sense = SenseHat()
        self.sense.set_imu_config(False, False, True)
        self.debugMode = False
        self.stopEvent = threading.Event()

    @pyqtSlot()
    def start(self):
        self.updateButtons.emit(False, True)
        self.stopEvent.clear()
        while not self.stopEvent.is_set():
            self.rotate_display()
            if self.debugMode == False:
                self.temperature = self.sense.get_temperature()
                self.humidity = self.sense.get_humidity()
                self.pressure = self.sense.get_pressure()

            self.updateLcd.emit(self.temperature, self.humidity, self.pressure)
            self.updateGraphs.emit(self.temperature, self.humidity, self.pressure, self.interval)
            self.show_temperature_on_led_matrix(self.temperature)
            self.log_to_file(self.temperature, self.humidity, self.pressure, self.filename)
            self.stopEvent.wait(timeout=(self.interval))

    def stop(self):
        self.stopEvent.set()

    def update_temperature(self, value):
        if self.debugMode == True:
            self.temperature = value

    def update_humidity(self, value):
        if self.debugMode == True:
            self.humidity = value

    def update_pressure(self, value):
        if self.debugMode == True:
            self.pressure = value

    def update_interval(self, value):
        self.interval = value

    def update_debug_mode(self, value):
        self.debugMode = value
        if value == True:
            self.filename = "log_debug.txt"
        else:
            self.filename = "log.txt"

    def log_to_file(self, temperature, humidity, pressure, filename):
        temperatureString = "{:.1f}°C".format(temperature)
        humidityString = "{:.0f}%".format(humidity)
        pressureString = "{:.0f}mbar".format(pressure)
        timeString = time.strftime("%d/%m/%Y %H:%M:%S")
        file = open(filename, "a")
        file.write(timeString + " | " + "Temperature: " + temperatureString + " | " + "Humidity: " + humidityString
                   + " | " + "Pressure: " + pressureString + "\n")
        file.close()

    def show_temperature_on_led_matrix(self, temp):
        positiveDegreeValue = 255 - temp * 5
        negativeDegreeValue = 255 + temp * 5

        if temp >= 0 and temp < 50:
            tempGrade = (255, positiveDegreeValue, positiveDegreeValue)

        elif temp < 0 and temp > -50:
            tempGrade = (negativeDegreeValue, negativeDegreeValue, 255)

        elif temp >= 50:
            tempGrade = (255, 0, 0)

        elif temp <= -50:
            tempGrade = (0, 0, 255)

        tempToString = "{:.1f}".format(temp)

        self.sense.show_message(tempToString + "c", back_colour=[0, 0, 0], text_colour=tempGrade)

    def rotate_display(self):
        x = round(self.sense.get_accelerometer_raw()['x'], 0)
        y = round(self.sense.get_accelerometer_raw()['y'], 0)

        rotation = 0
        if x == -1:
            rotation = 90
        elif y == -1:
            rotation = 180
        elif x == 1:
            rotation = 270

        self.sense.set_rotation(rotation)