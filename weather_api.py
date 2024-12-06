import requests

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.geocode_url = "http://api.openweathermap.org/geo/1.0/direct"

    def get_coordinates(self, city_name):
        """
        Lekéri a város koordinátáit a városnév alapján.
        """
        params = {
            "q": city_name,
            "limit": 1,  # Csak az első találatot adjuk vissza
            "appid": self.api_key,
        }

        try:
            response = requests.get(self.geocode_url, params=params)
            response.raise_for_status()
            data = response.json()

            if not data:
                print(f"Nincs találat a(z) '{city_name}' városnévhez.")
                return None, None

            # Első találat koordinátái
            return data[0]["lat"], data[0]["lon"]

        except requests.exceptions.RequestException as e:
            print(f"Hiba a geocoding API hívás során: {e}")
            return None, None

    def fetch_daily_forecast(self, latitude, longitude):
        """
        Lekéri az időjárási előrejelzést a következő 5 napra a koordináták alapján.
        """
        params = {
            "lat": latitude,
            "lon": longitude,
            "units": "metric",
            "appid": self.api_key,
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            # Napi előrejelzések kinyerése
            daily_forecast = []
            seen_dates = set()

            for item in data["list"]:
                # Csak az adott napot vesszük figyelembe
                date = item["dt_txt"].split(" ")[0]

                # Ha az adott napot még nem adtuk hozzá, hozzáadjuk
                if date not in seen_dates:
                    seen_dates.add(date)
                    weather = item["weather"][0]["description"]
                    min_temp = item["main"]["temp_min"]
                    max_temp = item["main"]["temp_max"]

                    daily_forecast.append({
                        "date": date,
                        "weather": weather,
                        "min_temp": min_temp,
                        "max_temp": max_temp,
                    })

                # Csak az első 5 napot vesszük figyelembe
                if len(daily_forecast) == 5:
                    break

            return daily_forecast

        except requests.exceptions.RequestException as e:
            print(f"Hiba az API hívás során: {e}")
            return None
