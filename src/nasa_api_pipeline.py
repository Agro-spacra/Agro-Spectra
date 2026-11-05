# src/nasa_api_pipeline.py
import requests
import pandas as pd
import json

def fetch_nasa_power_data(lat, lon, start_date="20260101", end_date="20261101"):
    """
    Fetches meteorological and soil parameters from the NASA POWER API
    for a given latitude, longitude, and date range.
    """
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,PRECTOTCORR,RH2M&community=AG&longitude={lon}&latitude={lat}&start={start_date}&end={end_date}&format=JSON"
    
    print(sending request to NASA POWER API for coordinates: ({lat}, {lon})...)
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        properties = data.get("properties", {}).get("parameter", {})
        df = pd.DataFrame(properties)
        print("Data successfully retrieved and processed.")
        return df
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

if __name__ == "__main__":
    # Example coordinates (e.g., agricultural region)
    latitude = 21.543
    longitude = 39.172
    
    df_weather = fetch_nasa_power_data(latitude, longitude)
    if df_weather is not None:
        print(df_weather.head())
        # Save sample output
        df_weather.to_csv("nasa_power_sample_output.csv")
