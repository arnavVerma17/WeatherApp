import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel,
    QLineEdit, QPushButton, QVBoxLayout
)
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.city_label = QLabel("Enter City")
        self.city_input = QLineEdit()
        self.get_weather_button = QPushButton("Get Weather")

        self.temperature_label = QLabel("")
        self.emoji_label = QLabel("")
        self.description_label = QLabel("")
        self.extra_info_label = QLabel("")

        self.initUI()

    def initUI(self):
        self.setWindowTitle("🌤 Weather App")
        self.setFixedSize(450, 650)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.emoji_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.extra_info_label)

        self.setLayout(layout)

        for widget in [
            self.city_label,
            self.city_input,
            self.temperature_label,
            self.emoji_label,
            self.description_label,
            self.extra_info_label,
        ]:
            widget.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("cityLabel")
        self.city_input.setObjectName("cityInput")
        self.get_weather_button.setObjectName("weatherButton")
        self.temperature_label.setObjectName("tempLabel")
        self.emoji_label.setObjectName("emojiLabel")
        self.description_label.setObjectName("descLabel")
        self.extra_info_label.setObjectName("extraLabel")

        self.setStyleSheet("""
            QWidget{
                background-color:#1E1E2F;
            }

            QLabel{
                color:white;
                font-family:Segoe UI;
            }

            QLabel#cityLabel{
                font-size:32px;
                font-weight:bold;
            }

            QLineEdit{
                font-size:22px;
                padding:12px;
                border-radius:10px;
                background:white;
            }

            QPushButton{
                font-size:22px;
                background:#4CAF50;
                color:white;
                border:none;
                border-radius:10px;
                padding:12px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#45a049;
            }

            QLabel#tempLabel{
                font-size:70px;
                font-weight:bold;
            }

            QLabel#emojiLabel{
                font-size:90px;
            }

            QLabel#descLabel{
                font-size:28px;
            }

            QLabel#extraLabel{
                font-size:20px;
                color:#d0d0d0;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "YOUR_API_KEY"   # <-- Replace with your API key

        city = self.city_input.text().strip()

        if city == "":
            self.display_error("Please enter a city name.")
            return

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric"
        )

        try:
            response = requests.get(url, timeout=10)
            data = response.json()

            if response.status_code == 200:
                self.display_weather(data)
            else:
                self.display_error(data.get("message", "Unknown Error").title())

        except requests.exceptions.ConnectionError:
            self.display_error("No Internet Connection")

        except requests.exceptions.Timeout:
            self.display_error("Request Timed Out")

        except Exception as e:
            self.display_error(str(e))

    def display_error(self, message):
        self.temperature_label.setText(message)
        self.temperature_label.setStyleSheet("font-size:28px;color:red;")
        self.emoji_label.clear()
        self.description_label.clear()
        self.extra_info_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet(
            "font-size:70px;color:white;font-weight:bold;"
        )

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        description = data["weather"][0]["description"].title()
        weather_id = data["weather"][0]["id"]
        city = data["name"]
        country = data["sys"]["country"]

        self.temperature_label.setText(f"{temp:.1f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(description)
        self.extra_info_label.setText(
            f"{city}, {country}\nHumidity: {humidity}%\nWind: {wind} m/s"
        )

    @staticmethod
    def get_weather_emoji(weather_id):

        if 200 <= weather_id <= 232:
            return "⛈️"

        elif 300 <= weather_id <= 321:
            return "🌦️"

        elif 500 <= weather_id <= 531:
            return "🌧️"

        elif 600 <= weather_id <= 622:
            return "❄️"

        elif 701 <= weather_id <= 741:
            return "🌫️"

        elif weather_id == 762:
            return "🌋"

        elif weather_id == 771:
            return "💨"

        elif weather_id == 781:
            return "🌪️"

        elif weather_id == 800:
            return "☀️"

        elif 801 <= weather_id <= 804:
            return "☁️"

        return "🌍"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())