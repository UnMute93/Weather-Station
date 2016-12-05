# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication

from WeatherStation import WeatherStation


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_station = WeatherStation(app)
    sys.exit(app.exec_())