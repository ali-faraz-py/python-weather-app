# Weather App project

import sys
import requests
from PyQt5.QtWidgets import (QMainWindow, QWidget, QApplication, QPushButton, QLabel, QLineEdit, 
                             QVBoxLayout, QHBoxLayout, QScrollArea)
from PyQt5.QtCore import Qt

class main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.hdl1 = QLabel("Weather App", self)
        self.CityName = QLabel("Please enter the city name", self)
        self.cityInput = QLineEdit(self)
        self.cityInput.setPlaceholderText("e.g., London, Tokyo, Paris")
        self.searchBt = QPushButton("search", self)
        self.errorInfo = QLabel(self)

        self.weather_container1 = QWidget(self)

        self.tempInfo = QLabel(self)
        self.displayImg = QLabel(self)
        self.descrip = QLabel(self)

        self.humidity_container = QWidget(self)

        self.humidity_title = QLabel("Humidity", self)
        self.humidity_info = QLabel(self)
        self.humidity_img = QLabel("💦", self)

        self.wind_container = QWidget(self)

        self.wind_title = QLabel("Wind", self)
        self.wind_info = QLabel(self)
        self.wind_img = QLabel("🌬️", self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        content_widget = QWidget()
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.hdl1)
        vbox.addWidget(self.CityName)
        vbox.addWidget(self.cityInput)
        vbox.addWidget(self.searchBt)
        vbox.addWidget(self.errorInfo)

        container1_layout = QVBoxLayout(self.weather_container1)       
        container1_layout.addWidget(self.tempInfo)
        container1_layout.addWidget(self.displayImg)
        container1_layout.addWidget(self.descrip)

        self.weather_container1.setLayout(container1_layout)
        self.weather_container1.hide()

        vbox.addWidget(self.weather_container1)

        hbox_info = QHBoxLayout()
        hbox_info.addWidget(self.humidity_container)
        hbox_info.addWidget(self.wind_container)
        vbox.addLayout(hbox_info)

        humidity_container1 = QVBoxLayout(self.humidity_container)
        humidity_container1.addWidget(self.humidity_title)
        humidity_container1.addWidget(self.humidity_info)
        humidity_container1.addWidget(self.humidity_img)

        self.humidity_container.setLayout(humidity_container1)
        self.humidity_container.hide()

        wind_container1 = QVBoxLayout(self.wind_container)
        wind_container1.addWidget(self.wind_title)
        wind_container1.addWidget(self.wind_info)
        wind_container1.addWidget(self.wind_img)

        self.wind_container.setLayout(wind_container1)
        self.wind_container.hide()

        content_widget.setLayout(vbox)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)

        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)

        self.hdl1.setObjectName("hdl1")
        self.CityName.setObjectName("CityName")
        self.cityInput.setObjectName("cityInput")
        self.searchBt.setObjectName("searchBt")
        self.errorInfo.setObjectName("errorInfo")
        self.weather_container1.setObjectName("weather_container1")
        self.tempInfo.setObjectName("tempInfo")
        self.displayImg.setObjectName("displayImg")
        self.descrip.setObjectName("descrip")
        self.humidity_title.setObjectName("humidity_title")
        self.humidity_info.setObjectName("humidity_info")
        self.humidity_img.setObjectName("humidity_img")
        self.wind_title.setObjectName("wind_title")
        self.wind_info.setObjectName("wind_info")
        self.wind_img.setObjectName("wind_img")
        self.humidity_container.setObjectName("humidity_container")
        self.wind_container.setObjectName("wind_container")

        self.hdl1.setAlignment(Qt.AlignCenter)
        self.CityName.setAlignment(Qt.AlignCenter)
        self.cityInput.setAlignment(Qt.AlignCenter)
        self.errorInfo.setAlignment(Qt.AlignCenter)
        self.tempInfo.setAlignment(Qt.AlignCenter)
        self.displayImg.setAlignment(Qt.AlignCenter)
        self.descrip.setAlignment(Qt.AlignCenter)
        self.humidity_title.setAlignment(Qt.AlignCenter)
        self.humidity_info.setAlignment(Qt.AlignCenter)
        self.humidity_img.setAlignment(Qt.AlignCenter)
        self.wind_title.setAlignment(Qt.AlignCenter)
        self.wind_info.setAlignment(Qt.AlignCenter)
        self.wind_img.setAlignment(Qt.AlignCenter)

        self.loadStylecss()

        self.searchBt.clicked.connect(self.getWeather)
        self.cityInput.returnPressed.connect(self.getWeather)

    def loadStylecss(self):
        try:
            with open("weatherapp.css", "r") as C:
                self.setStyleSheet(C.read())
        except FileNotFoundError:
            print("weatherapp.css not found!")

    def getWeather(self):
        api_key = "17a05a8da7586ded8fe284864ae71209"
        city = self.cityInput.text()
        
        if not city.strip():
            self.DisplayError("Please enter a city name")
            return
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.DisplayWeather(data)

        except requests.exceptions.HTTPError as HTTP_error:
            match response.status_code:
                case 400:
                    self.DisplayError("Bad Request:\nPlease check your input")
                case 401:
                    self.DisplayError("Unauthorized:\nInvalid API key")
                case 403:
                    self.DisplayError("Forbidden:\nAccess is denied")
                case 404:
                    self.DisplayError("Not Found:\nCity not found")
                case 500:
                    self.DisplayError("Internal Server Error:\nPlease try again later")
                case 502:
                    self.DisplayError("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.DisplayError("Service Unavailable:\nServer is down")
                case 504:
                    self.DisplayError("Gateway Timeout:\nNo response from server")
                case _:
                    self.DisplayError(f"HTTP Error Occured:\n{HTTP_error}")

        except requests.exceptions.ConnectionError:
            self.DisplayError("Connection Error:\nPlease check your internet connection")
        except requests.exceptions.Timeout:
            self.DisplayError("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.DisplayError("Too Many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.DisplayError(f"Request Error:\n{req_error}")


    def DisplayError(self, message):
        self.errorInfo.setText(message)
        self.displayImg.clear()
        self.descrip.clear()
        self.tempInfo.clear()
        self.weather_container1.hide()
        self.humidity_container.hide()
        self.wind_container.hide()


    def DisplayWeather(self, data):
        temperature_k = data['main']['temp']
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67
        weather_id = data['weather'][0]['id']
        temperature_descrip = data['weather'][0]['description']

        self.tempInfo.setText(f"{temperature_c:.0f}°C")
        self.displayImg.setText(self.weather_img(weather_id))
        self.descrip.setText(f"{temperature_descrip}")
        self.errorInfo.clear()

        self.weather_container1.show()
        self.humidity_container.show()
        self.wind_container.show()
        self.display_humidity(data)
        self.display_wind(data)

    def display_humidity(self, data):
        humid = data['main']['humidity']

        self.humidity_info.setText(f"{humid}%")

        self.errorInfo.clear()

    def display_wind(self, data):
        wind = data['wind']['speed']

        self.wind_info.setText(f"{wind} m/s")

        self.errorInfo.clear()


    @staticmethod
    def weather_img(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌩️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "🌬️"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = main_window()
    mainWindow.show()
    sys.exit(app.exec_())