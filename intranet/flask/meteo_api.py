import httpx

api = "https://api.open-meteo.com/v1/forecast?latitude=41.6941&longitude=44.8337&current=temperature_2m,precipitation,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max&timezone=auto&past_days=1"


# https://open-meteo.com/
class Weather:
    def get(self):
        data = httpx.get(api)

        return data.json()
