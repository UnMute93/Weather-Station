# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow

import ui_weather_station


class MainWindow(QMainWindow, ui_weather_station.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)