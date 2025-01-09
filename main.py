import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyWeather")
        self.setGeometry(710, 290, 500, 500)
        self.line_edit = QLineEdit(self)
        self.button = QPushButton("Submit",self)
        self.location_label = QLabel(self)
        self.temperature_label = QLabel(self)
        self.weather_icon_label = QLabel(self)
        self.error_label = QLabel(self)
        self.init_ui()
        

    def init_ui(self):
        # Set the overall stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;  /* Dark background for contrast */
            }
            QLabel#title {
                color: #f8f8f2;
                font-weight: bold;
                text-align: center;
                font-size: 28px;
            }
            QLabel#location {
                color: #8be9fd;
                font-size: 22px;
                font-weight: bold;
            }
            QLabel#temperature {
                color: #50fa7b;
                font-size: 18px;
            }
            QLabel#icon {
                color: #ffb86c;
                font-size: 90px;
                text-align: center;
            }
            QLabel#error {
                color: #ff5555;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QLineEdit {
                font-size: 20px;
                padding: 10px;
                border: 2px solid #6272a4;
                border-radius: 5px;
                color: #f8f8f2;
                background-color: #2e2e3e;
            }
            QLineEdit:focus {
                border-color: #8be9fd;
            }
            QPushButton {
                font-size: 18px;
                padding: 10px;
                border: 2px solid #6272a4;
                border-radius: 5px;
                color: #f8f8f2;
                background-color: #44475a;
            }
            QPushButton:hover {
                background-color: #6272a4;
            }
            QPushButton:pressed {
                background-color: #8be9fd;
            }
        """)

        # Title label
        title_label = QLabel("PyWeather", self)
        title_label.setFont(QFont("Arial", 24))
        title_label.setGeometry(10, 10, 480, 50)
        title_label.setObjectName("title")
        
        self.line_edit.setGeometry(10, 60, 360, 50)
        self.line_edit.setStyleSheet("font-size: 18px")

        self.button.setGeometry(390, 60, 100, 50)
        self.button.clicked.connect(self.submit)

        self.error_label.setFont(QFont("Arial", 14))
        self.error_label.setGeometry(10, 120, 480, 50)
        self.error_label.setObjectName("error")

        self.location_label.setFont(QFont("Arial", 20))
        self.location_label.setGeometry(10, 120, 480, 50)
        self.location_label.setObjectName("location")

        self.temperature_label.setFont(QFont("Arial", 18))
        self.temperature_label.setGeometry(10, 170, 480, 50)
        self.temperature_label.setObjectName("temperature")

        self.weather_icon_label.setFont(QFont("", 100))
        self.weather_icon_label.setGeometry(10, 210, 480, 100)
        self.weather_icon_label.setObjectName("icon")

    def submit(self):
        self.clear_display()
        text = self.line_edit.text()
        #print(f"{text}")
        # Display weather information
        try:
            location = get_location(text)
            #print(f"{location}")
            weather_data = get_weather(location)
            #print(f"{weather_data}")
            self.display_weather(weather_data, text)
        except Exception as e:
            
            self.display_error(f"Error fetching data: {e}")
            
            

    def display_weather(self, weather_data, name):
        self.location_label.setText(f"{name}")
        temp = weather_data.get("temperature", "N/A")
        self.temperature_label.setText(f"Current Temperature: {temp:.2f}°C")
        cloud_cover = weather_data.get("cloud_cover", 0)
        rain = weather_data.get("rain", 0)

        # Determine weather icon
        if cloud_cover > 60:
            icon = "☁"  # Cloudy
        elif cloud_cover > 20 and rain > 0.2:
            icon = "🌧"  # Rainy
        elif cloud_cover > 20:
            icon = "⛅"  # Partly Cloudy
        else:
            icon = "☀"  # Sunny

        self.weather_icon_label.setText(icon)
               
    def display_error(self, message):
        self.error_label.setText(f"{message}")

    def clear_display(self):
        # Clear weather and error labels
        self.location_label.clear()
        self.temperature_label.clear()
        self.weather_icon_label.clear()
        self.error_label.clear()


def get_weather(location_data):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location_data.get("latitude"),  # latitude
        "longitude": location_data.get("longitude"),  # longitude
        "current_weather": True,  # Request current weather data
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise error for bad responses
    data = response.json()
    
    current_weather = data.get("current_weather", {})
    return {
        "temperature": current_weather.get("temperature"),
        "rain": current_weather.get("precipitation", 0),
        "cloud_cover": current_weather.get("cloudcover", 0),
    }

def get_location(name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={name}&count=1&language=en&format=json"
    response = requests.get(url)
    response.raise_for_status()  # Raise error for bad responses
    data = response.json()

    # Check if results exist in the response
    results = data.get("results")
    if not results or len(results) == 0:
        raise ValueError(f"No location found for '{name}'")

    # Extract the first result
    location = results[0]
    return {
        "latitude": location.get("latitude"),
        "longitude": location.get("longitude"),
    }


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
