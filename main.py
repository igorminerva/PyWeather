import sys

import openmeteo_requests
import requests_cache
from retry_requests import retry

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyWeather")
        self.setGeometry(710,290,500,500)

    
        label = QLabel("PyWeather",self)
        label.setFont(QFont("Arial",20))
        label.setGeometry(10,10,500,100)

        info(self)
        

        
def info(self):
    label = QLabel("Porto Seguro",self)
    label.setFont(QFont("Arial",20))
    label.setGeometry(10,70,500,100)

    label = QLabel(f"Current temperature {get_meteo().Variables(0).Value(): .2f}",self)
    label.setFont(QFont("Arial",20))
    label.setGeometry(10,120,500,100)

    if get_meteo().Variables(2).Value() > 60:
        label = QLabel("☁",self)
        label.setFont(QFont("",70))
        label.setGeometry(10,170,500,100)
    
    elif get_meteo().Variables(2).Value() > 20 and get_meteo().Variables(1).Value() > 20:
        label = QLabel("🌧",self)
        label.setFont(QFont("",70))
        label.setGeometry(10,170,500,100)

    elif get_meteo().Variables(2).Value() > 20 and get_meteo().Variables(2).Value() < 60:
        label = QLabel("⛅",self)
        label.setFont(QFont("",70))
        label.setGeometry(10,170,500,100)



def get_meteo():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	"latitude": -16.4497,
	"longitude": -39.0647,
	"current": ["temperature_2m", "rain", "cloud_cover"],
	"forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    return current


def main():
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    


if __name__ == "__main__":
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    main()

